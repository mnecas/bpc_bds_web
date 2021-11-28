from django.test import TestCase
from main.models import Person
from django.contrib.auth.models import User


class UserTestCase(TestCase):
    def setUp(self):
        u = User.objects.create(
            username='username',
            first_name='first_name',
            last_name='last_name',
        )
        u.set_password('password')
        u.save()
        Person.objects.create(
            user=u,
            date_of_birth='1999-10-07',
            type='user'
        )

    def test_user_creation(self):
        person = Person.objects.get(id=1)
        self.assertEqual(person.user.username, 'username')
