from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    username = models.CharField(max_length=30, unique=False)
    email = models.EmailField(unique=True)

    def __str__(self):
        return 'User email: %s' % self.email


class Company(models.Model):
    name = models.CharField(max_length=30)
    url = models.SlugField(null=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE,)

    def __str__(self):
        return 'Company name: %s' % self.name


class Project(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    company = models.ForeignKey(Company, on_delete=models.CASCADE,)

    def __str__(self):
        return 'Project name: %s' % self.name


class State(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return 'State name: %s' % self.name


class Design(models.Model):
    value = models.DecimalField(max_digits=10, decimal_places=2)
    created_date = models.DateTimeField()
    process_file = models.ImageField(upload_to='process/', null=True, verbose_name="")
    original_file = models.ImageField(upload_to='original/', verbose_name="Design: ")
    designer_name = models.CharField(max_length=30)
    designer_last_name = models.CharField(max_length=30)
    designer_email = models.EmailField()
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return 'Design by: %s on %s' % (self.designer_name, self.created_date)
