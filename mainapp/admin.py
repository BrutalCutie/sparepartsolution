from mainapp.models import Request, Chat, Message, Filter, Store

from django.contrib import admin


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'car',
        'model',
        'year',
        'owner',

    )
    list_filter = (
        'car',
        'model',
        'owner',
    )
    search_fields = (
        'id',
        'car',
        'model',
        'year',
        'owner',
    )


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_by',
        'request',
        'is_active',

    )
    list_filter = (
        'request',
        "is_active"
    )
    search_fields = (
        "created_by",
        "request",
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "from_user",
        "chat",
        "to_user",
        'chat__request',

    )
    search_fields = (
        'message_text',
    )


@admin.register(Filter)
class FilterAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'filter_word',
    )


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'city',
        'address',
    )
