from django.test import TestCase

from mainapp.models import Request
from users.models import User


class RequestTestCase(TestCase):
    user = None
    test_data = {
        "car": "Ford",
        "model": "Focus",
        "year": 2008,
        "text": "test",
    }
    test_data_list = [
        {
            "car": "Ford",
            "model": "Focus",
            "year": 2008,
            "text": "test",
        },
        {
            "car": "Audi",
            "model": "A4",
            "year": 2015,
            "text": "test",
        },
    ]

    # создаём пользователя и насильно его авторизуем
    def setUp(self):
        self.user = User.objects.create(
            name="user1",
            email="user1@mail.com",
            phone="123",
        )
        self.client.force_login(user=self.user)

    def test_request_create(self):
        """
        создаем заявку и проверяем, что она создалась
        :return:
        """

        self.client.post(path="/request/create/", data=self.test_data)

        self.assertTrue(Request.objects.filter().exists())
        self.assertEqual(Request.objects.filter().first().owner, self.user)

    def test_request_update(self):
        """
        создаём и меняем заявку
        :return:
        """

        self.client.post(path="/request/create/", data=self.test_data)
        request = Request.objects.filter().first()
        self.client.post(
            path=f"/request/update/{request.pk}/",
            data={
                "car": "otherCar",
                "model": "otherFocus",
                "year": 2000,
                "text": "othertext",
            },
        )

        self.assertEqual(Request.objects.filter().first().car, "otherCar")

    def test_request_list(self):
        """
        тест создания и возврата списка queryset
        :return:
        """

        for data in self.test_data_list:
            self.client.post(path="/request/create/", data=data)

        r = self.client.get(path="/request/list/")
        self.assertEqual(len(r.context_data.get("requests")), 2)

    def test_request_delete(self):
        """
        удаление заявки
        :return:
        """
        self.client.post(path="/request/create/", data=self.test_data)

        created_request = Request.objects.get(car="Ford")

        self.client.delete(path=f"/request/delete/{created_request.pk}/")

        self.assertFalse(Request.objects.filter())


class RequestPermissionTestCase(TestCase):
    user = None
    test_data = {
        "car": "Ford",
        "model": "Focus",
        "year": 2008,
        "text": "test",
    }

    def setUp(self):
        self.user = User.objects.create(
            name="user1",
            email="user1@mail.com",
            phone="123",
        )
        self.user2 = User.objects.create(
            name="user2",
            email="user2@mail.com",
            phone="123",
        )

        self.client.force_login(user=self.user)

    def test_request_delete_by_other_user(self):
        """
        другой пользователь не может удалить чужую заявку
        :return:
        """
        self.client.post(
            path="/request/create/",
            data=self.test_data,
        )

        self.client.force_login(user=self.user2)

        request = Request.objects.get(car="Ford")
        self.assertTrue(request)

        self.client.delete(path=f"/request/delete/{request.pk}/")

        request = Request.objects.get(car="Ford")
        self.assertTrue(request)

    def test_request_update_by_other_user(self):
        """
        другой пользователь не может править чужую заявку
        :return:
        """
        self.client.post(
            path="/request/create/",
            data=self.test_data,
        )

        self.client.force_login(user=self.user2)

        request = Request.objects.get(car="Ford")

        self.client.post(
            path=f"/request/update/{request.pk}/",
            data={
                "car": "otherFord",
                "model": "otherFocus",
                "year": 2000,
                "text": "otherTest",
            },
        )

        self.assertTrue(Request.objects.get(car="Ford"))
