from django import template
from agriselect.models import CartItem  # Import your CartItem model

register = template.Library()

@register.simple_tag
def cart_item_count(user):
    if user.is_authenticated:
        return CartItem.objects.filter(user=user,status=CartItem.StatusChoices.ACTIVE).count()
    return 0