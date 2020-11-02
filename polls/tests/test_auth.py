from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class AuthenticationTests(TestCase):
    
    def setUp(self):
        User.objects.create_user(username='username', password='1101', email='mail@gmail.com')

    def test_login(self):
        response = self.client.post(reverse('login'), {'username': 'username', 'password': '1101'}, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_logout(self):
        self.client.login(username='username', password='1101')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test_login_wrong_password(self):
        response = self.client.post(reverse('login'), {'username': 'username', 'password': '1234'}, follow=True)
        self.assertFalse(response.context['user'].is_authenticated)