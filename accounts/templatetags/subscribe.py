from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def can_subscribe(user, subscription):
    if not user.subscription:
        return True
    if user.subscription.end_date < timezone.now():
        return True
    return False
