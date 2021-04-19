from django.db import models
from .base import Base
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext as _


class CHOICE:
    male = 0
    female = 1
    GENDER = ((male, _("Male")), (female, ("Female")))


class Location(models.Model):
    country = models.CharField(max_length=225, null=True)
    province = models.CharField(max_length=225, null=True)
    city = models.CharField(max_length=225, null=True)
    address = models.CharField(max_length=225, null=True)
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.updateAt = timezone.now()
        super().save(*args, **kwargs)


class Accounts(Base):
    avatar = models.ImageField(upload_to="accounts/")
    gender = models.IntegerField(choices=CHOICE.GENDER, default=CHOICE.male)
    phone_numbers = PhoneNumberField(null=True)
    is_banned = models.BooleanField(default=False)
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, null=False)

    def save(self, *args, **kwargs):
        self.updateAt = timezone.now()
        super().save(*args, **kwargs)
