from django.contrib import messages
from django.http import HttpResponse
from django.views.generic.edit import FormMixin
from django import forms


class SuccessMessageMixin:
    success_message: str = ''

    def form_valid(self, form: forms.BaseForm) -> HttpResponse:
        """Переопределяем метод валидации"""
        response = super().form_valid(form)  # type: ignore
        if self.success_message:
            messages.success(self.request, self.success_message)  # type: ignore
        return response
