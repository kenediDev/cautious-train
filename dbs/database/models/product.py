from django.db import models
from .user import Accounts
from django.utils import timezone
import uuid


class Category(models.Model):
    public_id = models.CharField(max_length=225, null=True, unique=True)
    name = models.CharField(max_length=225, null=False, unique=True)
    icon = models.ImageField(upload_to="category/")
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField()
    user = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    product_many = models.ManyToManyField(
        "Product", related_name="product_many_to_many")

    def save(self, *args, **kwargs):
        self.public_id = str(uuid.uuid4())
        self.updateAt = timezone.now()
        super().save(*args, **kwargs)


class Product(models.Model):
    public_id = models.CharField(max_length=225, null=True, unique=True)
    name = models.CharField(max_length=225, null=False, unique=True)
    photo = models.ImageField(upload_to="product/")
    sell = models.DecimalField(max_digits=12, decimal_places=2)
    promo = models.DecimalField(max_digits=12, decimal_places=2)
    agent = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.IntegerField(default=1)
    description = models.TextField()
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(null=True)
    author = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        self.public_id = str(uuid.uuid4())
        self.updateAt = timezone.now()
        super().save(*args, **kwargs)
