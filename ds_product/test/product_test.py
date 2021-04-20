import unittest
from django.utils.translation import gettext as _
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from database.models.product import Product, Category
from core.setup_test.setup import logger, readme
from django.core.files import File
from faker import Faker
from rest_framework_jwt.settings import api_settings

fake = Faker()


class ProductTester(unittest.TestCase):
    def setUp(self):
        self.e = APIClient()

    def test_p_a(self):
        logger.critical("Product Tester")

    def test_p_list(self):
        urls = reverse("product-list")
        response = self.e.get(urls, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        logger.info("Get all product")

    @unittest.skipIf(Product.objects.count() == 0, "Skip! Product not have data")
    def test_p_retrieve(self):
        product = Product.objects.first()
        urls = reverse("product-detail", args=[product.id])
        response = self.e.get(urls, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        logger.info('Get detail product')

    @unittest.skipIf(not readme.get('token') and Category.objects.count() == 0, 'Skip! missing token or Category not have data')
    def test_p_create(self):
        category = Category.objects.last()
        urls = reverse('product-list')
        payload = api_settings.JWT_PAYLOAD_HANDLER
        encode = api_settings.JWT_ENCODE_HANDLER
        token = encode(payload(category.user.user))
        data = {
            'name': fake.name(),
            'photo': File(open("prefix/1599307724_Attack-On-Titan-Season-4-Every-Detail.jpeg", "rb")),
            'sell': fake.random_number(),
            'promo': fake.random_number(),
            'agent': fake.random_number(),
            'description': fake.text(),
            'category': category.id,
            'author': category.user.id
        }
        self.e.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.e.post(urls, data)
        message = _("Product has been created")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {"message": message})
        logger.info(message)

    @unittest.skipIf(Product.objects.count() == 0, "Skip! product not have data")
    def test_p_update(self):
        product = Product.objects.first()
        urls = reverse('product-update', args=[product.id])
        payload = api_settings.JWT_PAYLOAD_HANDLER
        encode = api_settings.JWT_ENCODE_HANDLER
        token = encode(payload(product.author.user))
        data = {
            'name': fake.name(),
            'photo': File(open("prefix/1599307724_Attack-On-Titan-Season-4-Every-Detail.jpeg", "rb")),
            'sell': fake.random_number(),
            'promo': fake.random_number(),
            'agent': fake.random_number(),
            'description': fake.text(),
        }
        self.e.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.e.post(urls, data)
        message = _("Product has been updated")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': message})
        logger.info(message)

    @unittest.skipIf(Product.objects.count() == 0, "Skip! Product not have data")
    def test_p_destroy(self):
        product = Product.objects.first()
        urls = reverse("product-detail", args=[product.id])
        payload = api_settings.JWT_PAYLOAD_HANDLER
        encode = api_settings.JWT_ENCODE_HANDLER
        token = encode(payload(product.author.user))
        self.e.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.e.delete(urls, content_type='application/json')
        message = _("Product has been deleted")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': message})
        logger.info(message)
