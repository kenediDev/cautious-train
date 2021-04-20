from django.urls import path, include

urlpatterns = [
    path("user/", include("ds_user.urls.user")),
    path("product/", include("ds_product.urls.product"))
]
