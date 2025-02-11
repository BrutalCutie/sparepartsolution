from django.test import TestCase

from mainapp.models import Message, Request, Store
from users.models import User


class ChatTestCase(TestCase):
    user = None
    seller = None
    store = None

    def setUp(self):
        self.user = User.objects.create(
            name="user",
            email="user1@mail.com",
            phone="123",
        )

        self.store = Store.objects.create(
            name="TestStore",
            city="TestCity",
            address="TestAddress",
        )

        self.seller = User.objects.create(
            name="seller", email="seller1@mail.com", phone="123", is_seller=True, store=self.store
        )
        self.client.force_login(user=self.seller)

    def test_chat_and_message_create(self):
        request = Request.objects.create(
            owner=self.user, car="Ford", model="Focus", year=2008, text="Test", city="Ufa", city_not_matter=False
        )

        self.client.post(
            path=f"/request/detail/{request.pk}/new_message/",
            data={
                "message_text": "TestMessage",
            },
        )
        self.client.post(
            path=f"/chat/detail/{request.pk}/new_message/",
            data={
                "message_text": "TestMessage2",
            },
        )
        message1 = Message.objects.get(message_text="TestMessage")
        message2 = Message.objects.get(message_text="TestMessage2")

        self.assertTrue(message1)
        self.assertTrue(message2)
        self.assertTrue(message1.chat)
