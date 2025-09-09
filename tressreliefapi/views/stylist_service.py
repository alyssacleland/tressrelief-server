
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from tressreliefapi.models import StylistService

# GET /stylist-services?serviceId=:id
# StylistServiceLinks to pre-select stylists in the edit form
# as of now, not using this. leaving it here though.


class StylistServiceLinks(APIView):
    """Handle GET requests for stylist-service links of a specific service"""

    def get(self, request):
        service_id = request.query_params.get("serviceId")
        if not service_id:
            return Response([])

        ids = list(StylistService.objects
                   .filter(service_id=service_id)
                   .values_list("stylist_id", flat=True)
                   .order_by("stylist_id"))

        return Response(ids, status=status.HTTP_200_OK)
