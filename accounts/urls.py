from django.urls import path
from .views import CustomSignupView
from . import views

app_name = 'accounts'

urlpatterns = [
  path('login/', views.login, name='login'),
  path('logout/', views.logout, name='logout'),
  path('signup/', CustomSignupView.as_view(), name='signup'),
  path('email_overlap_check/', views.email_overlap_check, name='email_overlap_check'),
  path('delete/', views.delete, name='delete'),
  path('update/', views.update, name='update'),
  path('password/', views.change_password, name='change_password'),
  path('profile/<int:user_pk>/', views.profile, name='profile'),
  path('mydata/<int:user_pk>/', views.mydata, name='mydata'),
  path('subscribe/', views.subscribe, name='subscribe'),
]
