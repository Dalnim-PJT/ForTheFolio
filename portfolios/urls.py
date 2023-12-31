from django.urls import path
from . import views

app_name = 'portfolios'

urlpatterns = [
    # 제공하는 템플릿
    path('', views.index, name='index'),
    path('check/', views.check, name='check'),
    # path('<str:title>/', views.t_detail, name='t_detail'),
    # path('<str:title>/likes/', views.likes, name='likes'),
    # mydatas
    path('create/', views.m_create, name='m_create'),
    path('<str:mydata_title>/update/', views.m_update, name='m_update'),
    path('<str:mydata_title>/delete/', views.m_delete, name='m_delete'),
    # # portfolios
    path('<str:template_name>/create/', views.p_create, name='p_create'),
    path('<str:portfolio_name>/', views.p_detail, name='p_detail'),
    path('my_portfolio/<str:portfolio_name>/update/', views.p_update, name='p_update'),
    path('my_portfolio/<str:portfolio_name>/delete/', views.p_delete, name='p_delete'),
]
