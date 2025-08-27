from django.db import models

ROLE_CHOICES = (
    ("client", "Client"),
    ("stylist", "Stylist"),
    ("admin", "Admin")
)


class UserInfo(models.Model):

    # from google/firebase auth:
    uid = models.CharField(max_length=128, unique=True)
    # blank=True: means field not required (it's allowed to be blank)
    display_name = models.CharField(max_length=255, blank=True)
    google_email = models.EmailField(blank=True)
    photo_url = models.URLField(max_length=500, blank=True, null=True)
    # default or updated:
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,  # restricts values to the enum
        default="client",
    )
    # set only when obj is first created and saved to db
    created_at = models.DateTimeField(auto_now_add=True)
    # set every time obj is saved regardless
    updated_at = models.DateTimeField(auto_now=True)
