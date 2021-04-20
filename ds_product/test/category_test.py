import unittest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from database.models.product import Category
from core.setup_test.setup import readme, logger
from django.core.files import File
from faker import Faker
from django.utils.translation import gettext as _
from rest_framework_jwt.settings import api_settings

fake = Faker()


class CategoryTester(unittest.TestCase):
    def setUp(self):
        self.e = APIClient()

    def test_c_a(self):
        logger.critical("Category Tester")

    def test_c_list(self):
        urls = reverse("category-list")
        response = self.e.get(urls, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        logger.info("Get all category")

    @unittest.skipIf(not readme.get("token"), "Skip! missing token")
    def test_c_create(self):
        urls = reverse('category-list')
        decode = api_settings.JWT_DECODE_HANDLER
        token = readme.get('token')
        user = decode(token)
        data = {
            'name': fake.name(),
            'icon': File(open("prefix/1599307724_Attack-On-Titan-Season-4-Every-Detail.jpeg", "rb")),
            "user": user.get('user_id')
        }
        self.e.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.e.post(urls, data)
        message = _("Category has been created")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'message': message})
        logger.info(message)

    @unittest.skipIf(Category.objects.count() == 0, "Skip! Category not have data")
    def test_c_retrieve(self):
        category = Category.objects.first()
        urls = reverse('category-detail', args=[category.id])
        response = self.e.get(urls, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        logger.info("Get detail category")

    @unittest.skipIf(Category.objects.count() == 0, "Skip! Category not have data")
    def test_c_update(self):
        category = Category.objects.first()
        urls = reverse('category-update', args=[category.id])
        data = {
            'name': fake.name(),
            'icon': File(open("prefix/1599307724_Attack-On-Titan-Season-4-Every-Detail.jpeg", "rb")),
        }
        payload = api_settings.JWT_PAYLOAD_HANDLER
        encode = api_settings.JWT_ENCODE_HANDLER
        token = encode(payload(category.user.user))
        self.e.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.e.post(urls, data)
        message = _("Category has been updated")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': message})
        logger.info(message)

    @unittest.skipIf(Category.objects.count() == 0, "Skip! Category not have data")
    def test_c_destroy(self):
        category = Category.objects.first()
        payload = api_settings.JWT_PAYLOAD_HANDLER
        encode = api_settings.JWT_ENCODE_HANDLER
        token = encode(payload(category.user.user))
        urls = reverse('category-detail', args=[category.id])
        self.e.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.e.delete(urls, content_type='application/json')
        message = _("Category has been deleted")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': message})
        logger.info(message)
