"""Создаем представления для форм"""
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, TemplateView

from .forms import RegistrationForm, ChangePasswordForm


class RegistrationView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = 'account/registration.html'
    success_url = reverse_lazy('index-page')


class SigninView(LoginView):
    """Создаем вид для входа на сайт"""
    template_name = 'account/login.html'
    success_url = reverse_lazy('index-page')


class PasswordChangeView(LoginRequiredMixin, FormView):
    success_url = reverse_lazy('change-password-done')
    form_class = ChangePasswordForm
    template_name = 'account/change_password.html'
    login_url = reverse_lazy('login')

    def get_form_kwargs(self, **kwargs):
        """Чтобы передавать данные в обьект"""
        kwargs = super().get_form_kwargs()
        print(kwargs)
        kwargs['user'] = self.request.user
        print(kwargs)
        return kwargs

    def form_valid(self, form):
        """Здесь мы сохраняем данные"""
        form.save()
        return super().form_valid(form)


class PasswordChangeDoneView(TemplateView):  # TemplateVIew зависит только от шаблона
    """Здесь мы определяем вид при успешном изменении пароля
        Здесь мы определяем вид для изменения пароля
    """
    template_name = 'account/change_password_done.html'
