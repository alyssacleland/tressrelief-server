from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from tressreliefapi.views.auth import get_or_create_user

router = routers.DefaultRouter(trailing_slash=False)

urlpatterns = [
    path('', include(router.urls)),
    path("admin/", admin.site.urls),
    path("get-or-create-user", get_or_create_user),
]
