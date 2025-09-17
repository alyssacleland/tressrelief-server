from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from tressreliefapi.views import get_or_create_user, UserInfoView, CategoryView, ServiceView, OAuthCredentialViewSet
from tressreliefapi.views.oauth_status import oauth_google_status
from tressreliefapi.views.service_stylists_options import ServiceStylistOptions
from tressreliefapi.views.stylist_service import StylistServiceLinks
from tressreliefapi.views.oauth import oauth_google_initiate
from tressreliefapi.views.oauth_callback import oauth_google_callback

# The first parameter, r'userinfo, is setting up the url.
# The second UserInfoView is telling the server which view to use when it sees that url.
# The third, userinfo, is called the base name. You’ll only see the base name if you get an error in the server. It acts as a nickname for the resource and is usually the singular version of the url.

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'userinfo', UserInfoView, 'userinfo')
router.register(r'categories', CategoryView, 'category')
router.register(r'services', ServiceView, 'service')
router.register(r'oauth-credentials',
                OAuthCredentialViewSet, 'oauthcredential')


# Each path() in urlpatterns is mapping a URL pattern to a view — which is just the code that runs when someone visits that URL.
urlpatterns = [
    path('', include(router.urls)),
    path("admin/", admin.site.urls),
    path("get-or-create-user", get_or_create_user),
    path("stylist-services", StylistServiceLinks.as_view()),
    path("service-stylist-options", ServiceStylistOptions.as_view()),
    path("oauth/google/initiate", oauth_google_initiate),
    # the trailing slash is important below (in callback) because google will redirect to this exact url with the code query param added onto the end
    path("oauth/google/callback/", oauth_google_callback),
    path("oauth/google/status", oauth_google_status),
]
