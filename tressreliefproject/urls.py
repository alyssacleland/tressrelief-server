from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from tressreliefapi.views import get_or_create_user, UserInfoView, CategoryView, ServiceView


# The first parameter, r'userinfo, is setting up the url.
# The second UserInfoView is telling the server which view to use when it sees that url.
# The third, userinfo, is called the base name. You’ll only see the base name if you get an error in the server. It acts as a nickname for the resource and is usually the singular version of the url.

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'userinfo', UserInfoView, 'userinfo')
router.register(r'categories', CategoryView, 'category')
router.register(r'services', ServiceView, 'service')

# Each path() in urlpatterns is mapping a URL pattern to a view — which is just the code that runs when someone visits that URL.
urlpatterns = [
    path('', include(router.urls)),
    path("admin/", admin.site.urls),
    path("get-or-create-user", get_or_create_user),
]
