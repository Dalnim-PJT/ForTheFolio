from django.urls import path
from . import views

app_name = 'portfolios'

urlpatterns = [
    # 제공하는 템플릿
    path('', views.index, name='index'),
    # path('<str:title>/', views.t_detail, name='t_detail'),
    # path('<str:title>/likes/', views.likes, name='likes'),
    # mydatas
    path('create/', views.m_create, name='m_create'),
    path('<str:mydata_title>/update/', views.m_update, name='m_update'),
    # path('<str:mydata_title>/delete/', views.m_delete, name='m_delete'),
    # # portfolios
    # path('<str:title>/create/', views.p_create, name='p_create'),
    # path('<int:portfolio_pk>/', views.p_detail, name='p_detail'),
    # path('<int:portfolio_pk>/update/', views.p_update, name='p_update'),
    # path('<int:portfolio_pk>/delete/', views.p_delete, name='p_delete'),
]
