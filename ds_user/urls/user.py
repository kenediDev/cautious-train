from django.urls import path, include
from rest_framework import routers
from ds_user.views.user import UserModelViewSets, ResetAPIView, PasswordAPIView, UpdateAPIVIew, AvatarAPIView, BannedAPIView

router = routers.DefaultRouter()
router.register("", UserModelViewSets, basename="user")

urlpatterns = [
    path("", include(router.urls)),
    path("reset/password/", ResetAPIView.as_view(), name='user-reset'),
    path("update/password/", PasswordAPIView.as_view(), name='user-password'),
    path("update/accounts/", UpdateAPIVIew.as_view(), name='user-update'),
    path("update/accounts/avatar/", AvatarAPIView.as_view(), name='user-avatar'),
    path("banned/accounts/", BannedAPIView.as_view(), name="user-banned")
]
