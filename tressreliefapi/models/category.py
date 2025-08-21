from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=128)
    image_url = models.CharField(max_length=128)
    # set only when obj is first created and saved to db
    created_at = models.DateTimeField(auto_now_add=True)
    # set every time obj is saved regardless
    updated_at = models.DateTimeField(auto_now=True)
