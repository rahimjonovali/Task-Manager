from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, UserRegistrationView, current_user,TaskRetrieveUpdateDestroyAPIView,TaskListCreateAPIView


#router = DefaultRouter()
#router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    #path('', include(router.urls)),
    path('tasks/', TaskListCreateAPIView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskRetrieveUpdateDestroyAPIView.as_view(),name ='task-detail-view'),
    path('register/', UserRegistrationView.as_view(), name='api_register'),
    path('me/', current_user, name='current-users'),
]

