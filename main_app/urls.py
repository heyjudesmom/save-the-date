from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('dates/', views.dates_index, name='index'),
    path('dates/create/', views.DateCreate.as_view(), name='create_date'),
    path('dates/<int:date_id>/', views.dates_detail, name='detail'),
    path('dates/<int:pk>/update', views.DateUpdate.as_view(), name='dates_update'),
    path('dates/<int:pk>/delete', views.DateDelete.as_view(), name='dates_delete'),
    path('activity/', views.activity, name='activity'),
    path('accounts/signup/', views.signup, name='signup'),
]