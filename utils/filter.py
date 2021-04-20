import django_filters
from database.models.product import Product


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    sell = django_filters.CharFilter(lookup_expr="lte")

    class Meta:
        model = Product
        fields = ["name", "sell"]
