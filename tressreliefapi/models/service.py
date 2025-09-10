from django.db import models
from .category import Category


class Service(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=500, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    duration = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    image_url = models.CharField(max_length=300, blank=True)
    active = models.BooleanField(default=True)
    owner_uid = models.CharField(max_length=200, blank=True, null=True)
# set only when obj is first created and saved to db
    created_at = models.DateTimeField(auto_now_add=True)
    # set every time obj is saved regardless
    updated_at = models.DateTimeField(auto_now=True)
