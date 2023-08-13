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


@register.filter
def used_free(user):
    return user.payment_set.filter(subscription__title='1개월 무료').exists()

