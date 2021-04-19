from rest_framework import serializers


class BaseUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=225, required=False)
    email = serializers.CharField(max_length=225, required=False)
    first_name = serializers.CharField(max_length=225, required=False)
    last_name = serializers.CharField(max_length=225, required=False)
    old_password = serializers.CharField(max_length=225, required=False)
    password = serializers.CharField(max_length=225, required=False)
    confirm_password = serializers.CharField(max_length=225, required=False)

    class Meta:
        abstract = True


class BaseAccountsSerializer(serializers.Serializer):
    avatar = serializers.ImageField(required=False)
    gender = serializers.IntegerField(default=0, required=False)
    phone_numbers = serializers.CharField(max_length=225, required=False)

    class Meta:
        abstract = True


class BaseLocationSerializer(serializers.Serializer):
    country = serializers.CharField(max_length=225, required=False)
    province = serializers.CharField(max_length=225, required=False)
    city = serializers.CharField(max_length=225, required=False)
    address = serializers.CharField(max_length=225, required=False)

    class Meta:
        abstract = True


class Base(BaseUserSerializer, BaseAccountsSerializer, BaseLocationSerializer):
    class Meta:
        abstract = True
