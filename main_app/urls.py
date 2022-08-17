from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('dates/', views.dates_index, name='index'),
    path('dates/choose', views.choose_index, name='choose_index'),
    path('dates/create/', views.DateCreate.as_view(), name='create_date'),
    path('dates/<int:date_id>/', views.dates_detail, name='detail'),
    path('dates/<int:pk>/update', views.DateUpdate.as_view(), name='dates_update'),
    path('dates/<int:pk>/delete', views.DateDelete.as_view(), name='dates_delete'),
    path('dates/<int:date_id>/add_photo/', views.add_photo, name='add_photo'),
    path('dates/<int:date_id>/assoc_activity/<int:activity_id>', views.assoc_activity, name='assoc_activity'),
    path('dates/<int:date_id>/unassoc_activity/<int:activity_id>', views.unassoc_activity, name='unassoc_activity'),
    path('activity/', views.activity, name='activity'),
    path('activity/<int:pk>/delete', views.ActivityDelete.as_view(), name='activities_delete'),
    path('activity/create/', views.create_activity, name='create_activity'),
    path('accounts/signup/', views.signup, name='signup'),

]