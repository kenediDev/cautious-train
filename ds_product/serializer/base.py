from rest_framework import serializers
from database.models.user import Accounts
from database.models.product import Category


class BaseCategorySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=225, required=False)
    icon = serializers.ImageField(required=False)
    user = serializers.PrimaryKeyRelatedField(
        queryset=Accounts.objects.all(), required=False)

    class Meta:
        abstract = True


class BaseProductSerializer(serializers.Serializer):
    photo = serializers.ImageField(required=False)
    sell = serializers.DecimalField(
        max_digits=12, decimal_places=2, required=False)
    promo = serializers.DecimalField(
        max_digits=12, decimal_places=2, required=False)
    agent = serializers.DecimalField(
        max_digits=12, decimal_places=2, required=False)
    description = serializers.CharField(required=False)
    author = serializers.PrimaryKeyRelatedField(
        queryset=Accounts.objects.all(), required=False)
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), required=False)

    class Meta:
        abstract = True


class Base(BaseCategorySerializer, BaseProductSerializer):
    class Meta:
        abstact = True
