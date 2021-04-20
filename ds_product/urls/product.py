from django.urls import path, include
from rest_framework import routers
from ds_product.views.product import CategoryModelViewSets, UpdateCategoryAPIView, ProductModelViewSets, UpdateProductAPIView, ProductListAPIView

router = routers.DefaultRouter()
router.register("category", CategoryModelViewSets, basename='category')
router.register("", ProductModelViewSets, basename="product")

urlpatterns = [
    path("update/product/<pk>/",
         UpdateProductAPIView.as_view(), name='product-update'),
    path("update/category/<pk>/",
         UpdateCategoryAPIView.as_view(), name='category-update'),
    path("", include(router.urls)),
    path('retrieve/all/', ProductListAPIView.as_view(), name="product-all")
]
