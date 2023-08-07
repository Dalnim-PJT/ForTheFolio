from django.shortcuts import render, get_object_or_404, redirect
from .models import Subscription, Payment
from datetime import timedelta
from django.utils import timezone
from django.http import HttpResponseForbidden
from django.contrib import messages

# Create your views here.
def index(request):
    subscriptions = Subscription.objects.all()
    context = {
        'subscriptions': subscriptions
    }

    return render(request, 'payments/index.html', context)


def subscribe(request, subscription_id):
    if request.method == 'POST':
        subscription = get_object_or_404(Subscription, id=subscription_id)

        if subscription.title == '1 개월 무료' and Payment.objects.filter(user=request.user, price__title='1 개월 무료').exists():
            return HttpResponseForbidden("이미 1개월 무료 구독을 사용하셨습니다.")
        
        start_date = timezone.now()
        duration_map = {'1MF': 1, '1M': 1, '3M': 3, '6M': 6, '1Y': 12}
        duration_months = duration_map.get(subscription.title, 1)
        end_date = start_date + timedelta(days=30 * duration_months)
        
        payment = Payment(user=request.user, price=subscription, start_date=start_date, end_date=end_date)
        payment.save()

        request.user.subscription = payment
        request.user.save()

        return redirect('accounts:profile', request.user.pk)
    else:
        return redirect('payments:index')