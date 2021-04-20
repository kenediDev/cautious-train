from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

api_info = openapi.Info(
    title="Kenedi (API)",
    default_version='v1',
    description="Open API",
    terms_of_service="",
    contact=openapi.Contact(email="lymad@yahoo.com"),
    license=openapi.License(name="BSD License"),
)

schema_view = get_schema_view(
    api_info,
    public=True,
    permission_classes=[permissions.AllowAny, ]
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("authtoken/", obtain_jwt_token, name="authtoken"),
    path("refresh-authtoken/", refresh_jwt_token, name="refresh-authtoken"),
    path("verify-authtoken/", verify_jwt_token, name="verify-authtoken"),
    path("api/v1/", include("core.urls")),
    path('swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(
        cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
