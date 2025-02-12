from rest_framework import serializers

from mainapp.models import Chat, Message, Request


class RequestSerializer(serializers.ModelSerializer):
    """
    Сериалайзер заявок
    """
    class Meta:
        model = Request
        fields = "__all__"


class ChatSerializer(serializers.ModelSerializer):
    """
    Сериалайзер чатов
    """
    class Meta:
        model = Chat
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    """
    Сериалайзер сообщений
    """
    class Meta:
        model = Message
        fields = "__all__"
