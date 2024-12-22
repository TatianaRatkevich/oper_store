from django.urls import path
from django.contrib.auth import views as auth_views
from .views import index_view, MyLoginView, store_tasks_view, operator_tasks_view, role_based_redirect_view

urlpatterns = [
    path('', index_view, name='index'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('store/', store_tasks_view, name='store_index'),
    path('operator/', operator_tasks_view, name='operator_index'),
    path('role-redirect/', role_based_redirect_view, name='role_redirect'),

]