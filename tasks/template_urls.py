from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list_view, name='task_list'),
    path('tasks/<int:pk>/', views.task_detail_view, name='task_detail'),
    path('tasks/new/', views.task_create_view, name='task_create'),
    path('tasks/<int:pk>/edit/', views.task_update_view, name='task_update'),
    path('tasks/<int:pk>/delete/', views.task_delete_view, name='task_delete'),
]

