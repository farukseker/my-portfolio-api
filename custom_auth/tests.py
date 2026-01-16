import time
from django.test import TestCase
from django.shortcuts import reverse, resolve_url
from django.contrib.auth.models import User
from config.settings import test
from requests import api
from faker import Faker


class AuthTest(TestCase):
    def setUp(self):
        self.fake = Faker()
        self.bad_user_credentials = {
            'username': self.fake.user_name(),
            'password': self.fake.password(),
            'email': self.fake.password()
        }
        self.bad_user = User.objects.create_user(**self.bad_user_credentials)

        self.admin_user_credentials = {
            'username': self.fake.user_name(),
            'password': self.fake.password(),
            'email': self.fake.password()
        }

        self.admin_user = User.objects.create_superuser(**self.admin_user_credentials)

    def test_bad_user_cant_login_admin_panel(self):
        self.client.login(**self.bad_user_credentials)
        response = self.client.get(reverse('api:custom_admin:page-manage'))
        self.assertEqual(response.status_code, 403)

    def test_jwt_refresh(self):
        self.client.login(**self.admin_user_credentials)
        test_url = f'{test.MACHINE_IP}{reverse('api:custom_admin:page-manage')}'
        login_url_token = resolve_url(reverse('api:auth:token_obtain_pair'))
        p = api.post(login_url_token, {
            'username': 'echo', 'password': 'ratatatata01!'
        })
        response = self.client.get(reverse('api:custom_admin:page-manage'))
        self.assertEqual(response.status_code, 200)
        time.sleep(2)

        response = self.client.get(reverse('api:custom_admin:page-manage'))
        self.assertEqual(response.status_code, 401)
