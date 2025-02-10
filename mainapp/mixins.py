from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import render


class IsSellerMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_seller:
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        return render(self.request, 'mainapp/access_denied.html')


class IsModelOwnerMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().owner != self.request.user:
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        return render(self.request, 'mainapp/access_denied.html')


class IsChatMember(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        chat = self.get_object()

        if self.request.user not in [chat.created_by, chat.request.owner]:
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        return render(self.request, 'mainapp/access_denied.html')
