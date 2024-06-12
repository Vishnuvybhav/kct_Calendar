from django.db import models
from django.contrib.auth.models import User
from django import forms

# Create your models here.
class Event(models.Model):
    COLLEGES = [
        ('KCT', 'KCT'),
        ('KCLAS', 'KCLAS'),
        ('KCBS', 'KCBS'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    college = models.CharField(max_length=200, choices=COLLEGES)
    location = models.CharField(max_length=200)
    category = models.ManyToManyField('Category')
    is_disabled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='events_created')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='events_updated')
    

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=200, default="#000000")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='categories_created')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='categories_updated')

    def __str__(self):
        return self.name

class Colabrations(models.Model):
    colabrator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='colaborations_as_colaborator')
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, related_name='colaborations')
    access_levels = models.ManyToManyField('AccessLevels')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='colaborations_created')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='colaborations_updated')

    def __str__(self):
        return self.colabrator.username

class AccessLevels(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='access_levels_created')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='access_levels_updated')

    def __str__(self):
        return self.name
