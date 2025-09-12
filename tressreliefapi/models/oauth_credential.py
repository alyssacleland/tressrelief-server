from django.db import models
from .user_info import UserInfo

# this model will store stylists tokens when they connect google, w/ a rule that each stylist can only have one set for google. with these tokens saved, the server can: 1
# 1.) read the stylists busy times and generate available slots for clients
# 2.) create/update/cancel events on the stylists calendar


class OAuthCredential(models.Model):
    # links the credentials to which stylist they belong to
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    # provider is needed for the unique pair (user + provider) so I can't accidentally save 2 google connections for the same stylist
    provider = models.CharField(max_length=32, default='google')
    # refresh token: is the key i keep long-term. lets the server get new access tokens when the old ones expire, without the stylist having to log in again
    refresh_token = models.TextField()
    # access token: is short-lived, usually expires in an hour.will overwrite whenever i refresh it using the refresh token. This is needed for making api calls to google on behalf of the stylist.
    # text fields can hold larger strings than char fields
    access_token = models.TextField(blank=True, null=True)
    # token expiry: when the access token will expire. let's me check if it is still valid before making api calls to google, and if not, refresh it using the refresh token first
    token_expiry = models.DateTimeField(blank=True, null=True)
    # which calendar to write to. using 'primary' for simplicity. will use when creating/updating/deleting events on the stylist's google calendar
    calendar_id = models.CharField(max_length=255, default='primary')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'provider'], name='unique_user_provider')
            # db guard so that each stylist can only have one set of credentials for each provider (google). prevents duplicates that would break availability/event logic
        ]
