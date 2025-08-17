from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from django.contrib.auth import get_user_model

from .models import Task
from .serializers import TaskSerializer, UserSerializer
from .permissions import IsOwner
from .forms import TaskForm, CustomUserCreationForm,ProfileUpdateForm

User = get_user_model()

class  ProfileUpdateView(LoginRequiredMixin,UpdateView):
	model = User
	form_class = ProfileUpdateForm
	template_name = "profile/profile_form.html"
	success_url = reverse_lazy('profile')

	def get_object(self, queryset=None):
		return self.request.user

	def form_valid(self, form):
		messages.success(self.request, "Profile updated successfully")
		return super().form_valid(form)

class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer

	def get_permissions(self):
		if self.action == 'create':
			return [permissions.AllowAny()]  # anyone can register
		return [permissions.IsAuthenticated(), IsOwner()]

	def get_queryset(self):
		user = self.request.user
		if user.is_staff:  # Admin can see all users
			return User.objects.all()
		return User.objects.filter(id=user.id)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(user=user)






@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Account created successfully")
        return redirect('task_list')


class TaskListView(LoginRequiredMixin, ListView):
	model = Task
	template_name = 'tasks/task_list.html'
	context_object_name = 'tasks'
	def get_queryset(self):
		status_filter = self.request.GET.get('status', '')
		queryset = Task.objects.filter(user=self.request.user)
		if status_filter:
			queryset = queryset.filter(status=status_filter)
		return queryset

class TaskDetailView(LoginRequiredMixin,DetailView):
	model = Task
	template_name = 'tasks/task_detail.html'
	context_object_name = 'task'

	def get_queryset(self):
		return Task.objects.filter(user=self.request.user)

class TaskCreateView(LoginRequiredMixin, CreateView):
	model = Task
	form_class = TaskForm
	template_name = 'tasks/task_form.html'

	def form_valid(self,form):
		form.instance.user = self.request.user
		messages.success(self.request, 'Task created successfully!')
		return super().form_valid(form)
	def get_success_url(self):
		return reverse_lazy('task_detail', kwargs={'pk': self.object.pk})


class TaskUpdateView(LoginRequiredMixin,UpdateView):
	model = Task
	form_class = TaskForm
	template_name = 'tasks/task_form.html'

	def get_queryset(self):
		return Task.objects.filter(user=self.request.user)

	def form_valid(self, form):
		messages.success(self.request, 'Task updated successfully!')
		return super().form_valid(form)

	def get_success_url(self):
		return reverse_lazy('task_detail', kwargs={'pk': self.object.pk})

class TaskDeleteView(LoginRequiredMixin, DeleteView):
	model = Task
	template_name = 'tasks/task_delete.html'
	context_object_name = 'task'
	success_url = reverse_lazy('task_list')

	def get_queryset(self):
		return Task.objects.filter(user=self.request.user)

	def delete(self,request, *args, **kwargs):
		messages.success(self.request, 'Task deleted successfully!')
		return super().delete(request, *args, **kwargs)


