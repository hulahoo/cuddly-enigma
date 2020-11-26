"""Здесь мы будем записывать url нашей регистрации"""
from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import RegistrationView, SigninView, PasswordChangeView, PasswordChangeDoneView

urlpatterns = [
    path('signup/', RegistrationView.as_view(), name='signup'),
    path('signin/', SigninView.as_view(), name='signin'),
    path('signout/', LogoutView.as_view(), name='signout'),  # для выхода из учетной записи нам не нужно создавать форму и вид так ка в джанго уже есть готовый класс
    path('change_password/', PasswordChangeView.as_view(), name='change-password'),
    path('change_password_done/', PasswordChangeDoneView.as_view(), name='change-password-done')
]
