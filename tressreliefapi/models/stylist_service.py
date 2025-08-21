from django.db import models
from tressreliefapi.models import Service, UserInfo


class StylistService(models.Model):
    stylist = models.ForeignKey(
        UserInfo, on_delete=models.CASCADE, related_name="stylist_services")
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="service_stylists"
    )

    # so you can't duplicate the same link:
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["stylist", "service"],
                name="unique_stylist_service"
            )
        ]
