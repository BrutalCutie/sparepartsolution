from rest_framework.permissions import BasePermission

from mainapp.models import Chat


class IsChatMember(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        chat_pk = request.parser_context.get("kwargs", {}).get("chat_pk")
        chat = Chat.objects.get(pk=chat_pk)

        return user in [chat.created_by, chat.request.owner]
