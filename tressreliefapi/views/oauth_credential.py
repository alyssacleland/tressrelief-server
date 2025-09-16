from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from tressreliefapi.models import OAuthCredential
from tressreliefapi.serializers.oauth_credential import OAuthCredentialSerializer


class OAuthCredentialViewSet(viewsets.ModelViewSet):
    """
    CRUD for OAuth credentials.
    """
    queryset = OAuthCredential.objects.all()
    serializer_class = OAuthCredentialSerializer
    permission_classes = []
