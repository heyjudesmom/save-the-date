from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('dates/', views.dates, name='dates'),
    path('dates/create/', views.create_date, name='create_date'),
    path('activity/', views.activity, name='activity'),
    path('accounts/signup/', views.signup, name='signup'),
]