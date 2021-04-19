from rest_framework import serializers
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from ds_user.serializer.base import Base
from database.models.user import Location, Accounts
import re
from django.db.models import Q
from django.core.mail import EmailMessage
import dotenv
import os

dotenv.load_dotenv()

r_email = r"username = serializers.CharField(max_length=225, required=False)"


class UserSerializer(Base):
    def __init__(self, instance=None, data=None, **kwargs):
        super().__init__(instance=instance, data=data, **kwargs)

    def get_fields(self, *args, **kwargs):
        fields = super(UserSerializer, self).get_fields(*args, **kwargs)
        return fields

    def create(self, validated_data):
        if self.context['args'] == "create":
            self.c_u(validated_data)
        return validated_data

    def c_u(self, options):
        self.f_already(options.get('username'))
        self.f_already(options.get('email'))
        if options.get('password') != options.get('confirm_password'):
            raise serializers.ValidationError(
                _("Password don't match, please check again"))
        create = User(username=options.get('username'), email=options.get(
            'email'), password=options.get('password'))
        create.set_password(options.get('confirm_password'))
        create.save()
        location = Location()
        location.save()
        create.accounts_set.create(location=location)
        return create

    def f_already(self, options):
        check = User.objects.filter(
            Q(username=options) | Q(email=options)).first()
        if check:
            choice = "Username"
            if re.search(r_email, options):
                choice = "Email"
            raise serializers.ValidationError(
                _("%s already exists, please choose another one") % choice)
        return check

    @classmethod
    def r_u(cls, options):
        check = User.objects.filter(
            Q(username=options) | Q(email=options)).first()
        if not check:
            return False
        mail = EmailMessage("Subjects", "Hello Worlds",
                            os.environ.get('smtp_user'), [check.email])
        return mail.send()

    def update(self, instance, validated_data):
        if self.context['args'] == 'password':
            return self.u_p(validated_data, instance)
        if self.context['args'] == 'update':
            return self.u_a(validated_data, instance)
        return instance

    def u_p(self, options, context):
        if not context.check_password(options.get('old_password')):
            raise serializers.ValidationError("Wrong password")
        if options.get('password') != options.get('confirm_password'):
            raise serializers.ValidationError(
                "Password don't match, please check again")
        context.set_password(options.get('confirm_password'))
        context.save()
        return context

    def u_a(self, options, context):
        context.first_name = options.get('first_name')
        context.last_name = options.get('last_name')
        self.accounts(options, context)
        context.save()
        return context

    def accounts(self, options, context):
        accounts = context.accounts_set.first()
        if options.get('avatar'):
            if accounts.avatar:
                try:
                    split = str(accounts.avatar).split("/")
                    path = "media/accounts/%s" % split[len(split) - 1]
                    os.system("rm %s" % path)
                except OSError:
                    pass
            accounts.avatar = options.get('avatar')
        accounts.gender = options.get('gender')
        accounts.phone_numbers = options.get('phone_numbers')
        accounts.save()
        self.location(options, accounts)
        return accounts

    def location(self, options, context):
        location = context.location
        location.country = options.get('country')
        location.province = options.get('province')
        location.city = options.get('city')
        location.address = options.get('address')
        location.save()
        return location

    @classmethod
    def avatar(cls, options, context):
        accounts = context.accounts_set.first()
        if accounts.avatar:
            splits = str(accounts.avatar).split("/")
            path = "media/accounts/%s" % splits[len(splits) - 1]
            os.system("rm %s" % path)
        accounts.avatar = options.get('avatar')
        accounts.save()
        return accounts

    @classmethod
    def banned(cls, options):
        accounts = Accounts.objects.filter(user__id=options).first()
        accounts.is_banned = True if not accounts.is_banned else False
        accounts.save()
        return accounts


class LocationModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class AccountsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = "__all__"


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
