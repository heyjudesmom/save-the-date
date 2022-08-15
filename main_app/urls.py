from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('dates/', views.index, name='index'),
    path('dates/create/', views.DateCreate.as_view(), name='create_date'),
    path('activity/', views.activity, name='activity'),
    path('accounts/signup/', views.signup, name='signup'),
]