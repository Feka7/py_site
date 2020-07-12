from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('new_user/', views.user_new, name='user_new'),
    path('login/', views.log, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('last_hour/', views.post_last_hour, name='last_hour'),
    path('report/', views.report, name='report'),
    path('admin_view/', views.admin_view, name='admin_view'),
    path('utente/<int:pk>/', views.utente, name='utente')
]
