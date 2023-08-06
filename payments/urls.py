from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [
    path('', views.index, name='index'),
    path('subscribe/<int:subscription_id>/', views.subscribe, name='subscribe'),
]