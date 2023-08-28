from django.shortcuts import render, get_object_or_404, redirect
from .models import Subscription, Payment
from datetime import timedelta
from django.utils import timezone
from django.http import HttpResponseForbidden
import requests
import os
from dateutil.relativedelta import relativedelta

ADMIN_KEY = os.getenv('ADMIN_KEY')
JS_KEY = os.getenv('JS_KEY')

# Create your views here.
def index(request):
    subscriptions = Subscription.objects.all()
    context = {
        'subscriptions': subscriptions,
        'JS_KEY': JS_KEY,
    }

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'payments/index.html', context)

    return render(request, 'payments/index.html', context)


def subscribe(request, subscription_id):
    if request.method == 'POST':
        subscription = get_object_or_404(Subscription, id=subscription_id)

        if subscription.title == '첫 달 무료' and Payment.objects.filter(user=request.user, price__title='첫 달 무료').exists():
            return HttpResponseForbidden("이미 첫 달 무료 구독을 사용하셨습니다.")
        
        start_date = timezone.now()
        duration_map = {'1MF': 1, '1M': 1, '3M': 3, '6M': 6, '1Y': 12}
        duration_months = duration_map.get(subscription.title, 1)
        end_date = start_date + timedelta(days=30 * duration_months)
        
        payment = Payment(user=request.user, subscription=subscription, start_date=start_date, end_date=end_date)
        payment.save()

        request.user.subscription = payment
        request.user.save()

        return redirect('accounts:profile', request.user.pk)
    else:
        return redirect('payments:index')
    

def kakaopay(request, subscription_id):
    if request.method == "POST":
        subscription = get_object_or_404(Subscription, id=subscription_id)
        price = subscription.price

        url = f'https://kapi.kakao.com/v1/payment/ready'
        headers = {
            'Authorization': f'KakaoAK {ADMIN_KEY}',
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
        }
        data = {
            'cid': 'TC0ONETIME',
            'partner_order_id': subscription.pk, # 주문번호
            'partner_user_id': request.user.pk, # 사용자
            'item_name': subscription.title, # 제품명
            'quantity': '1',
            'total_amount': price,
            'tax_free_amount':'0',
            'approval_url':f'http://127.0.0.1:8000/payments/{subscription.pk}/pay_success/', 
            'fail_url':'http://127.0.0.1:8000/payments/pay_fail',
            'cancel_url':'http://127.0.0.1:8000/payments/pay_cancel'
        }
        res = requests.post(url, data=data, headers=headers)
        result = res.json()
        if result.get('msg') == 'onetime order should have amount!':
            start_date = timezone.now()
            end_date = start_date + relativedelta(months=subscription.months)

            payment = Payment.objects.create(user=request.user, subscription=subscription, start_date=start_date, end_date=end_date)

            request.user.subscription = payment
            request.user.save()

            return redirect('accounts:profile', request.user.pk)
        else:
            request.session['tid'] = result['tid']
            return redirect(result['next_redirect_pc_url'])
    return redirect('payments:index')


def pay_success(request, subscription_id):
    subscription = get_object_or_404(Subscription, id=subscription_id)
    url = 'https://kapi.kakao.com/v1/payment/approve'
    
    headers = {
        'Authorization': f'KakaoAK {ADMIN_KEY}',
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
    }
    data = {
        'cid':'TC0ONETIME',
        'tid': request.session['tid'], # 결제고유번호
        'partner_order_id': subscription.pk,
        'partner_user_id': request.user.pk,
        'pg_token': request.GET['pg_token'] 
    }
    res = requests.post(url, data=data, headers=headers)
    result = res.json()

    start_date = timezone.now()
    end_date = start_date + relativedelta(months=subscription.months)

    payment = Payment.objects.create(user=request.user, subscription=subscription, start_date=start_date, end_date=end_date)

    request.user.subscription = payment
    request.user.save()

    context = {
        'res': res,
        'result': result,
    }

    return render(request, 'payments/pay_success.html', context)


def pay_fail(request):
    return render(request, 'payments/pay_fail.html')


def pay_cancel(request):
    return render(request, 'payments/pay_cancel.html')