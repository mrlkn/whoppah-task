from typing import Union

from rest_framework import serializers

from . import choices
from .models import Category, Product
from .utils import is_valid_transition


class BaseSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    last_updated_by = serializers.SerializerMethodField()

    def get_created_by(self, obj) -> Union[str, None]:
        return obj.created_by.email if obj.created_by else None

    def get_last_updated_by(self, obj) -> Union[str, None]:
        return obj.last_updated_by.email if obj.last_updated_by else None


class CategorySerializer(BaseSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ("slug",)

    def create(self, validated_data: dict):
        user = self.context["request"].user
        return Category.objects.create(created_by=user, **validated_data)

    def update(self, instance, validated_data: dict):
        user = self.context["request"].user
        instance.last_updated_by = user
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class ProductSerializer(BaseSerializer):
    """
    Serializer for Product model.
    """

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ("slug", "state")

    def create(self, validated_data: dict) -> Product:
        """
        Create a new product instance.

        Args:
            validated_data (dict): Validated data for creating a new product.

        Returns:
            Product: The newly created product instance.
        """
        user = self.context["request"].user
        product = Product.objects.create(
            created_by=user, state=choices.DRAFT, **validated_data
        )
        return product


class ProductStateUpdateSerializer(serializers.Serializer):
    state = serializers.ChoiceField(choices=choices.STATE_CHOICES)

    def validate_state(self, attrs: str) -> str:
        user = self.context.get("user")
        new_state = attrs

        if self.instance.state == new_state:
            raise serializers.ValidationError(
                "Given state is same as the current state."
            )

        if not is_valid_transition(self.instance, new_state, user):
            raise serializers.ValidationError("Can not perform this transition.")
        return attrs

    def update(self, instance: Product, validated_data: dict) -> Product:
        user = self.context.get("user")
        new_state = validated_data.get("state")

        instance.state = new_state
        instance.last_updated_by = user
        instance.save()

        return instance
