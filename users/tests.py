from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user

from .forms import UserRegistrationForm



class UserRegistrationTestCase(TestCase):
    def test_user_account_is_created(self):
        self.client.post(
            reverse('users:register'),
            data={
                'username': 'testuser',
                'email': 'test@mail.com',
                'password': 'testpassword123'
            }
        )

        user = User.objects.get(username='testuser')
        self.assertEqual(user.email, 'test@mail.com')
        self.assertTrue(user.check_password('testpassword123'))
        self.assertNotEqual(user.password, 'testpassword123') 

    def test_required_fields(self):
        response = self.client.post(reverse('users:register'), {})  
        self.assertEqual(response.status_code, 200) 
        self.assertIn('conForm', response.context)  
        form = response.context['conForm']
        self.assertTrue(form.errors)
        self.assertIn('username', form.errors)
        self.assertIn('This field is required.', form.errors['username'])

    def test_invalid_email(self):
        response = self.client.post(
            reverse('users:register'),
            data={
                'username': 'testuser',
                'email': 'invalid-email',
                'password': 'testpassword123'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('conForm', response.context)
        form = response.context['conForm']
        self.assertTrue(form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('Enter a valid email address.', form.errors['email'])

    def test_unique_username(self):
        User.objects.create_user(username='userbek',email='a@mail.com', password='password123')
        response = self.client.post(
            reverse('users:register'),
            data={
                'username': 'userbek',
                'email': 'a@mail.com',
                'password': 'testpassword123'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('conForm', response.context)
        form = response.context['conForm'] 
        self.assertTrue(User.objects.filter(username='userbek').count() == 1)
        self.assertTrue(form.errors)
        self.assertIn('username', form.errors)
        self.assertIn('A user with that username already exists.', form.errors['username'])
    

class UserLoginTestCase(TestCase):
    def setUp(self):
        usr = User.objects.create_user(username='userbek',email='test@mail.com')
        usr.set_password('testpassword123')
        usr.save()

    def test_successful_login(self):
        response = self.client.post(
            reverse('users:login'),
            data={
                'username': 'userbek',
                'password': 'testpassword123'
            }
        )
        self.assertEqual(response.status_code, 302)

        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_unsuccessful_login(self):
        response = self.client.post(
            reverse('users:login'),
            data={
                'username': 'xato-userbek',
                'password': 'testpassword123'
            }
        )
        self.assertEqual(response.status_code, 200)
        
        user= get_user(self.client)
        self.assertFalse(user.is_authenticated)

        response = self.client.post(
            reverse('users:login'),
            data={
                'username': 'userbek',
                'password': 'xato-testpassword123'
            }
        )
        self.assertEqual(response.status_code, 200)
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)
    
    def test_logout(self):
        self.client.login(username='userbek', password='testpassword123')
        response = self.client.get(reverse('users:logout'))
        self.assertEqual(response.status_code, 302)
        userbek = get_user(self.client)
        self.assertFalse(userbek.is_authenticated)


class UserProfileTestCase(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/users/login/'))

    def test_profile_view(self):
        user = User.objects.create(username='userbek',email='test@mail.com')
        user.set_password('testpassword123')
        user.save()
        self.client.login(username='userbek', password='testpassword123')
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'userbek')
        self.assertContains(response, 'test@mail.com')

    def test_profile_edit(self):
        user = User.objects.create(username='userbek',email='test@mail.com',first_name='Userjon',last_name='Usertoyev')
        user.set_password('<PASSWORD>')
        user.save()

        self.client.login(username='userbek', password='<PASSWORD>')
        response = self.client.post(reverse('users:profile'), data={'username': 'usera', 'email': 'test1@mail.com','first_name': 'Userjon','last_name': 'Usertoyev'})
        self.assertEqual(response.status_code, 302)
        user.refresh_from_db()
        self.assertEqual(user.first_name, 'Userjon')
        self.assertEqual(user.last_name, 'Usertoyev')
        self.assertEqual(user.email, 'test1@mail.com')
        self.assertEqual(user.username, 'usera')



