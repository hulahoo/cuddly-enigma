"""Здесь мы будем создавать формы для регистрации и для этого импортируем forms"""
from django import forms
from django.contrib.auth.models import User


class RegistrationForm(forms.ModelForm):
    """Класс для регистрационного поля"""
    password = forms.CharField(min_length=1, required=True, widget=forms.PasswordInput)
    password_confirm = forms.CharField(min_length=1, required=True, widget=forms.PasswordInput)

    class Meta:
        """Здесь мы перечесляем поля"""
        model = User  # здесь мы передаем поля для User
        fields = ('username', 'password', 'password_confirm', 'first_name', 'last_name', 'email')

    def clean_username(self):
        """Здесь мы валидируем данные пользователя"""
        username = self.cleaned_data.get('username')
        if User.objects.filter(username='username').exists():
            raise forms.ValidationError('This username already exists')
        return username

    def clean(self):
        """Проверка пароля на схожесть"""
        data = self.cleaned_data  # это всегда словарь поэтому мы получаем значения из него с помощью get
        password = data.get('password')
        password_confirm = data.pop('password_confirm')
        if password != password_confirm:
            raise forms.ValidationError("Password is not the same")
        return data  # и в итоге data возвращает нам словарь с даными пользователя

    def save(self, commit=True):
        """commit = true для того чтобы сразу отправлял запись в базу. Здесь мы сохраняем данные"""
        user = User.objects.create_user(**self.cleaned_data)  # две звездочки нужны для распоковки словаря cleaned_data
        return user  # обьект save должен всегда что то возвращать


class ChangePasswordForm(forms.Form):
    """Здесь мы пишем форму для изменения пароля"""
    old_password = forms.CharField(required=True, widget=forms.PasswordInput)
    password = forms.CharField(min_length=1, required=True, widget=forms.PasswordInput)
    password_confirm = forms.CharField(min_length=1, required=True, widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        """Проверка старого пароля с новым введеным"""
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError("Entered password is not correct")
        return old_password

    def clean(self):
        """Проверка пароля на схожесть"""
        data = self.cleaned_data  # это всегда словарь поэтому мы получаем значения из него с помощью get
        password = data.get('password')
        password_confirm = data.pop('password_confirm')
        if password != password_confirm:
            raise forms.ValidationError("Password is not the same")
        return data  # и в итоге data возвращает нам словарь с даными пользователя

    def save(self, commit=True):
        """Сохраняем пароль"""
        password = self.cleaned_data['password']
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user
