from django.db.models import Q
from django.shortcuts import render
from django.views.generic import DetailView, ListView, View
from .models import Product, Category, Comment


def test_view(request):
    """Тестовая вьюшка"""
    return render(request, 'mainapp/index.html', {})


class IndexPage(ListView):
    """главная страница"""
    model = Category
    template_name = 'mainapp/index.html'
    context_object_name = 'categories'


class ProductListView(ListView):
    """листинг постов"""
    paginate_by = 3
    model = Product
    template_name = 'mainapp/index.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('q')
        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(description__icontains=search))
        return queryset


class ProductDetailView(DetailView):
    model = Product
    template_name = 'mainapp/product_detail.html'
    context_object_name = 'product'


class CommentView(View):
    """Пишем вьюшку для коментариев"""
    model = Comment
    template_name = 'mainapp/product_detail.html'
    context_object_name = 'comment'