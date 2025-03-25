from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Task
import json
from datetime import date

class TaskAPITestCase(TestCase):
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='testpassword1'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpassword2'
        )
        
        # Create test tasks
        self.task1 = Task.objects.create(
            title='Test Task 1',
            description='Description for test task 1',
            status='TODO',
            due_date=date(2023, 12, 31),
            user=self.user1
        )
        
        self.task2 = Task.objects.create(
            title='Test Task 2',
            description='Description for test task 2',
            status='IN_PROGRESS',
            due_date=date(2023, 11, 30),
            user=self.user2
        )
        
        # Initialize API client
        self.client = APIClient()
    
    def test_get_tasks_authenticated(self):
        """Test that an authenticated user can get their tasks"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(reverse('task-list'))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Task 1')
    
    def test_get_tasks_unauthenticated(self):
        """Test that an unauthenticated user cannot get tasks"""
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_task(self):
        """Test creating a new task"""
        self.client.force_authenticate(user=self.user1)
        data = {
            'title': 'New Task',
            'description': 'Description for new task',
            'status': 'TODO',
            'due_date': '2023-12-15'
        }
        response = self.client.post(reverse('task-list'), data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 3)
        self.assertEqual(Task.objects.get(title='New Task').user, self.user1)
    
    def test_update_task(self):
        """Test updating an existing task"""
        self.client.force_authenticate(user=self.user1)
        data = {
            'title': 'Updated Task 1',
            'status': 'DONE'
        }
        response = self.client.patch(
            reverse('task-detail', kwargs={'pk': self.task1.id}),
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.title, 'Updated Task 1')
        self.assertEqual(self.task1.status, 'DONE')
    
    def test_delete_task(self):
        """Test deleting a task"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(reverse('task-detail', kwargs={'pk': self.task1.id}))
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 1)
    
    def test_user_cannot_access_others_tasks(self):
        """Test that a user cannot access another user's tasks"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(reverse('task-detail', kwargs={'pk': self.task2.id}))
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

