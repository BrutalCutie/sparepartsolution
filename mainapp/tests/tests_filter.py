from django.test import TestCase

from mainapp.models import Request, Chat, Message, Filter, Store
from users.models import User


class FilterTestCase(TestCase):
    user = None

    def setUp(self):
        self.user = User.objects.create(
            name='user1',
            email='user1@mail.com',
            phone='123',

        )
        self.client.force_login(user=self.user)

    def test_filter_create(self):
        """
        создаем фильтр
        :return:
        """

        self.client.post(
            path='/users/filters/',
            data={
                'filter_word': 'TestFilter'
            }
        )

        self.assertTrue(
            Filter.objects.get(filter_word="TestFilter")
        )
