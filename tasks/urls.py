from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, current_user,UserViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    # path('register/', UserRegistrationView.as_view(), name='api_register'),
    path('me/', current_user, name='current-users'),
]

