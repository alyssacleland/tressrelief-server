from django.db import models


class UserInfo(models.Model):
    class Roles(models.TextChoices):  # enum helper for string fields
        CLIENT = "client", "Client", "CLIENT"
        STYLIST = "stylist", "Stylist", "STYLIST"
        ADMIN = "admin", "Admin", "ADMIN"

    # from google/firebase auth:
    uid = models.CharField(max_length=128, unique=True)
    # blank=True: means field not required (it's allowed to be blank)
    display_name = models.CharField(max_length=255, blank=True)
    google_email = models.EmailField(blank=True)
    # default or updated:
    role = models.CharField(
        max_length=20,
        choices=Roles.choices,  # restricts values to the enum
        default=Roles.CLIENT,
    )
    # set only when obj is first created and saved to db
    created_at = models.DateTimeField(auto_now_add=True)
    # set every time obj is saved regardless
    updated_at = models.DateTimeField(auto_now=True)
