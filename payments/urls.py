from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [
    path('', views.index, name='index'),
    path('subscribe/<int:subscription_id>/', views.subscribe, name='subscribe'),
    path('<int:subscription_id>/kakaopay/', views.kakaopay, name='kakaopay'),
    path('<int:subscription_id>/pay_success/', views.pay_success, name='pay_success'),
    path('pay_fail/', views.pay_fail, name='pay_fail'),
    path('pay_cancel/', views.pay_cancel, name='pay_cancel'),
]