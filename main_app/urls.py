from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('home/', views.home, name='home'),
    path('activity/', views.activity, name='activity'),
    path('accounts/signup/', views.signup, name='signup'),
]