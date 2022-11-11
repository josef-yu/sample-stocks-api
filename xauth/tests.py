from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse
from django.contrib.auth.models import User

# Create your tests here.

SUPER_USERNAME = 'admin'
SUPER_PASSWORD = 'admin1234'
SUPER_EMAIL = 'test@test.com'

class CreateUserTest(APITestCase):
    def setUp(self):
        self.super_user = User.objects\
            .create_superuser(
                username=SUPER_USERNAME,
                email=SUPER_EMAIL,
                password=SUPER_PASSWORD
            )
        self.client.login(username=SUPER_USERNAME, password=SUPER_PASSWORD)
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.base_data = {
            'username': 'sampleuser',
            'password': 'samplepass1234'
        }
        self.data = self.base_data.copy()
        self.data['email'] = 'sample@email.com'
    
    def test_can_create_user(self):
        register_response = self.client.post(self.register_url, self.data)
        login_response = self.client.post(self.login_url, self.base_data)
        login_response_json = login_response.json()

        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertTrue(login_response_json['auth_token'] is not None)


        
