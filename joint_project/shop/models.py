from django.db import models

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=255)
    is_actual = models.BooleanField(default=True)

class Shop(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=255)
    count = models.IntegerField(null=True)
    price = models.IntegerField(null=True)
    is_actual = models.BooleanField(default=True)
    categories = models.ForeignKey('Category', null=True, on_delete=models.CASCADE)