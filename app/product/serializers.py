from typing import Union

from rest_framework import serializers

from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    last_updated_by = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ('slug',)

    def create(self, validated_data: dict) -> Category:
        user = self.context['request'].user
        category = Category.objects.create(created_by=user, **validated_data)
        return category

    def update(self, instance: Category, validated_data: dict) -> Category:
        user = self.context['request'].user
        instance.last_updated_by = user

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def get_created_by(self, obj: Category) -> Union[str]:
        return obj.created_by.email if obj.created_by else None

    def get_last_updated_by(self, obj: Category) -> Union[str]:
        return obj.last_updated_by.email if obj.last_updated_by else None


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'price', 'category', 'state']
