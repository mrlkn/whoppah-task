from transitions import Machine


class ProductStateMachine:

    def __init__(self, product, user):
        self.product = product
        self.user = user

        self.machine = Machine(model=self, initial=product.state)

        self.machine.add_transition(trigger='to_new', source='draft', dest='new')
        self.machine.add_transition(trigger='reject', source='new', dest='rejected', conditions=['is_admin'])
        self.machine.add_transition(trigger='ban', source='new', dest='banned', conditions=['is_admin'])
        self.machine.add_transition(trigger='accept', source='new', dest='accepted', conditions=['is_admin'])
        self.machine.add_transition(trigger='return_to_new', source='rejected', dest='new', conditions=['is_creator'])

    def is_admin(self):
        return self.user.is_staff

    def is_creator(self):
        return self.product.created_by == self.user
