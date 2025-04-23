from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
import datetime

class CustomUser(AbstractUser):
	avatar = models.ImageField(upload_to="users/avatar", null=True,blank=True)
	headline = models.CharField(max_length=100, null=True, blank=True)
	bio = models.TextField(null=True, blank=True)
	email = models.EmailField(max_length=50, unique=True)
	username = None
	birth_date = models.DateField(null=True,blank=True)

	@property
	def name(self):
		return f"{self.first_name} {self.last_name}"
	@property
	def age(self):
		today = datetime.date.today()
		return today.year - self.birth_date.year

	def __str__(self):
		return self.first_name

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []
	objects = CustomUserManager()


