from django.test import TestCase
from main.models import Person
import bcrypt


class UserTestCase(TestCase):
    def setUp(self):
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw("pass1234".encode('utf-8'), salt)
        Person.objects.create(
            date_of_birth='1999-10-07',
            type='user',
            username='username',
            first_name='first_name',
            last_name='last_name',
            password=password_hash
        )

    def test_user_creation(self):
        person = Person.objects.get(id=1)
        self.assertEqual(bcrypt.checkpw("pass1234".encode('utf-8'), person.password), True)
