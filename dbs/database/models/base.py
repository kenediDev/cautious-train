from django.db import models
from django.contrib.auth.models import User


class BaseForeignKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class BaseSoft(models.Model):
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class BaseTimeStamps(models.Model):
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField()

    class Meta:
        abstract = True


class Base(BaseForeignKey, BaseSoft, BaseTimeStamps):
    class Meta:
        abstract = True
