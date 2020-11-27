from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, View, CreateView, UpdateView, DeleteView
from django.views.generic.base import ContextMixin

from .forms import AddCommentForm, EditPost, PaymentForm
from .models import Product, Category, Comment, Payment


def test_view(request):
    """Тестовая вьюшка"""
    return render(request, 'mainapp/index.html', {})


class IndexPage(ListView):
    """главная страница"""
    model = Category  # берем модельку категории
    template_name = 'mainapp/index.html'  # указываем по какому html
    context_object_name = 'categories'  # здесь мы указываем имя для связии с шаблоном


class ProductListView(ListView):
    """листинг постов"""
    paginate_by = 3  # пагинация 3 продуктов на странице
    model = Product
    template_name = 'mainapp/index.html'
    context_object_name = 'products'

    def get_queryset(self):
        """Здесь мы определяем поиск"""
        queryset = super().get_queryset()  # переопределяем родительский метод
        search = self.request.GET.get('q')  # создаем переменную в которой мы берем из запроса с помощью GET по ключу запрос который нам прилетает
        if search:  # если есть такое значение
            queryset = queryset.filter(Q(title__icontains=search) | Q(description__icontains=search))  # здесь мы фильтруем по Q запросу по названию и описанию
        return queryset  # в противном случае мы выводим queryset


class ProductDetailView(DetailView):
    model = Product
    template_name = 'mainapp/product_detail.html'
    context_object_name = 'product'


class CommentView(View):
    """Пишем вьюшку для коментариев"""
    model = Comment
    template_name = 'mainapp/product_detail.html'
    context_object_name = 'comment'


class ContextMixin:
    """Мы определяем один метод который нужен для всех классов"""
    def get_context_data(self, *args, **kwargs):
        """придаем логику в метод миксина"""
        context = super().get_context_data(*args, **kwargs)
        context['comment_form'] = self.get_form(self.get_form_class())
        return context


class CommentCreateView(LoginRequiredMixin, ContextMixin, CreateView):
    """добавление поста"""
    model = Comment
    template_name = 'mainapp/comment_create.html'
    form_class = AddCommentForm

    def form_valid(self, form):
        """выполняется в том случае если все правильно."""
        comment = self.model.objects.create(user=self.request.user, **form.cleaned_data)  # берет model и обьект который создаем и вызывает мет create(где берет пользователя через request
        return redirect(comment.get_absolute_url())


class UpdateCommentView(ContextMixin, UpdateView):
    """изменение поста"""
    model = Comment
    template_name = 'mainapp/comment_update.html'
    form_class = EditPost
    context_object_name = 'comment'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise Http404
        return obj


class DeleteCommentView(DeleteView):
    """удаление поста"""
    model = Comment
    template_name = 'mainapp/comment_delete.html'
    success_url = reverse_lazy('index-page')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise Http404
        return obj

class PaymentView(View):
    model = Payment
    form_class = PaymentForm
    def get(self, *args, **kwargs):
        return render(self.request, 'mainapp/payment.html')


class PaymentConfirmationView(View):
    model = Payment
    template_name = 'mainapp/payment_finished.html'
