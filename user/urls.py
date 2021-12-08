from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterUser.as_view(), name='user-register'),
    path('login/', views.LogIn.as_view(), name='user-login')
]