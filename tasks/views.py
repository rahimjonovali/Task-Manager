from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect,HttpResponse

from rest_framework import viewsets, permissions, status,mixins
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from django.contrib.auth.models import User

from .models import Task
from .serializers import TaskSerializer, UserSerializer
from .permissions import IsOwner
from .forms import TaskForm, CustomUserCreationForm

# The following view is not used in urls.py
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(user=user)
#These following two views are alternative for the above one !!!!!
class TaskListCreateAPIView(mixins.ListModelMixin,
			    mixins.CreateModelMixin,
			    generics.GenericAPIView):
	queryset = Task.objects.all()
	serializer_class = TaskSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		return Task.objects.filter(user=self.request.user)
	def get(self, request, *args, **kwargs):
		return self.list(request, *args, **kwargs)
	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)

class TaskRetrieveUpdateDestroyAPIView(mixins.RetrieveModelMixin,
				       mixins.UpdateModelMixin,
				       mixins.DestroyModelMixin,
				       generics.GenericAPIView):
	queryset = Task.objects.all()
	serializer_class = TaskSerializer
	permission_class = [permissions.IsAuthenticated]

	def get_queryset(self):
		return Task.objects.filter(user=self.request.user)
	def get(self, request, *args, **kwargs):
		return self.retrieve(request, *args, **kwargs)
	def put(self, request, *args, **kwargs):
		return self.update(request, *args, **kwargs)
	def patch(self, request, *args, **kwargs):
		return self.partial_update(request, *args, **kwargs)
	def delete(self, request, *args, **kwargs):
		return self.destroy(request, *args, **kwargs)

class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

# Template Views
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('task_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

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
#@login_required
#def task_delete_view(request, pk):
#    task = get_object_or_404(Task, pk=pk, users=request.users)
#    if request.method == 'POST':
#        task.delete()
#        messages.success(request, 'Task deleted successfully!')
#        return redirect('task_list')
#    return redirect('task_detail', pk=pk)

