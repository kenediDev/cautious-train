from database.models.user import CHOICE
import unittest
from rest_framework import status
from django.utils.translation import gettext as _
from rest_framework.test import APIClient
from django.contrib.auth.models import User
import json
from faker import Faker
from core.setup_test.setup import logger, readme
from django.urls import reverse
from django.core.files import File
import random
from rest_framework_jwt.settings import api_settings


fake = Faker()


class UserTester(unittest.TestCase):
    def setUp(self):
        self.e = APIClient()

    def test_usr_a(self):
        logger.critical("User Tester")

    @unittest.skipIf(User.objects.count() == 0, "user not have data")
    def test_usr_login(self):
        user = User.objects.first()
        urls = reverse('authtoken')
        data = json.dumps({
            'username': user.username,
            'password': 'Password'
        })
        response = self.e.post(urls, data, content_type='application/json')
        with open("core/setup_test/requirements.json", "w") as w:
            w.write(json.dumps({'token': response.data.get('token')}))
        self.assertNotEqual(response.data.get('token'), None)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        logger.info('Login user')

    @unittest.skipIf(not readme.get('token'), 'Skip! missing token')
    def test_usr_refresh(self):
        urls = reverse('refresh-authtoken')
        data = json.dumps({
            'token': readme.get('token')
        })
        response = self.e.post(urls, data, content_type='application/json')
        with open("core/setup_test/requirements.json", "w") as w:
            w.write(json.dumps({'token': response.data.get('token')}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data.get('token'), None)
        logger.info('Refresh token')

    @unittest.skipIf(not readme.get('token'), 'Skip! missing token')
    def test_usr_verify(self):
        urls = reverse('verify-authtoken')
        data = json.dumps(
            {'token': readme.get('token')})
        response = self.e.post(urls, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data.get('token'), None)
        logger.info('Verify token')

    def test_usr_create(self):
        urls = reverse('user-list')
        data = json.dumps({
            'username': fake.name(),
            'email': fake.email(),
            'password': "Password",
            'confirm_password': "Password"
        })
        response = self.e.post(urls, data, content_type='application/json')
        message = _("Accounts has been created")
        self.assertEqual(response.data, {'message': message})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        logger.info(message)

    @unittest.skipIf(not readme.get('token'), "Skip! missing token")
    def test_usr_list(self):
        urls = reverse('user-list')
        self.e.credentials(HTTP_AUTHORIZATION="Bearer " + readme.get('token'))
        response = self.e.get(urls, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data, None)
        logger.info("Get all user")

    @unittest.skipIf(not readme.get('token'), "Skip! missing token")
    def test_usr_detail(self):
        count = User.objects.count()
        user = None
        if count > 2:
            user = User.objects.filter(id=count-1).first()
        else:
            user = User.objects.first()
        self.e.credentials(HTTP_AUTHORIZATION="Bearer " + readme.get('token'))
        urls = reverse('user-detail', args=[user.id])
        response = self.e.get(urls, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data, None)
        logger.info("Detail user")

    @unittest.skipIf(User.objects.count() == 0, "Skip! user not have data")
    def test_usr_reset(self):
        user = User.objects.first()
        urls = reverse('user-reset')
        data = json.dumps({
            'token': user.email
        })
        response = self.e.post(urls, data, content_type='application/json')
        message = _("Accounts has been reset")
        self.assertEqual(
            response.data, {'message': message})
        self.assertNotEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        logger.info(message)

    @unittest.skipIf(not readme.get('token'), "Skip! missing token")
    def test_usr_pwrd(self):
        urls = reverse('user-password')
        data = json.dumps({
            'old_password': "Password",
            'password': "Password",
            'confirm_password': "Password"
        })
        self.e.credentials(HTTP_AUTHORIZATION="Bearer " + readme.get('token'))
        response = self.e.post(urls, data, content_type='application/json')
        message = _("Password has been updated")
        self.assertEqual(
            response.data, {"message": message})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        logger.info(message)

    @unittest.skipIf(not readme.get('token'), 'Skip! missing token')
    def test_usr_acc_uptd(self):
        urls = reverse('user-update')
        data = {
            'first_name': fake.name(),
            'last_name': fake.name(),
            'avatar': File(open("prefix/1599307724_Attack-On-Titan-Season-4-Every-Detail.jpeg", "rb")),
            'gender': CHOICE.male,
            'phone_numbers': '+628%s' % random.randint(93999, 939489),
            'country': fake.country(),
            'province': fake.state(),
            'city': fake.city(),
            'address': fake.address()
        }
        self.e.credentials(HTTP_AUTHORIZATION="Bearer " + readme.get('token'))
        response = self.e.post(urls, data, follow=True)
        message = _("Profile has been updated")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, {"message": message})
        logger.info(message)

    @unittest.skipIf(not readme.get('token'), "Skip! missing token")
    def test_usr_avatar(self):
        urls = reverse('user-avatar')
        self.e.credentials(HTTP_AUTHORIZATION="Bearer " + readme.get('token'))
        data = {
            'avatar': File(open("prefix/1599307724_Attack-On-Titan-Season-4-Every-Detail.jpeg", "rb"))
        }
        response = self.e.post(urls, data, follow=True)
        message = _("Profile has been updated")
        self.assertEqual(
            response.data, {"message": message})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        logger.info(message)

    @unittest.skipIf(not readme.get("token"), "Skip! missing token")
    def test_usr_prohibited(self):
        admin = User.objects.filter(is_superuser=True).first()
        payload = api_settings.JWT_PAYLOAD_HANDLER(admin)
        encode = api_settings.JWT_ENCODE_HANDLER(payload)
        urls = reverse("user-banned")
        data = json.dumps({
            "token": User.objects.first().id
        })
        self.e.credentials(HTTP_AUTHORIZATION="Bearer " + encode)
        response = self.e.post(urls, data, content_type='application/json')
        message = _("Accounts has been banned")
        self.assertEqual(response.data, {"message": message})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        logger.info(message)
