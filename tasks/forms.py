from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth import get_user_model
from .models import Task

User = get_user_model()

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

class CustomUserCreationForm(UserCreationForm):
     class Meta:
        model = User
        fields = ['email', 'first_name', 'password1', 'password2']
        labels = {'birth_date': 'Date of Birth','headline': 'Your Headline','bio': 'Short Bio',}
        help_texts = {'avatar': 'Optional profile picture',}


class ProfileUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = "__all__"
        labels = {'birth_date': 'Date of Birth', 'headline': 'Your Headline', 'bio': 'Short Bio', }
        help_texts = {'avatar': 'Optional profile picture', }
