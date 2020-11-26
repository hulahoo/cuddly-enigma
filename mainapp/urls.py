""""""
from django.urls import path

from .views import test_view, ProductDetailView, ProductListView

urlpatterns = [
    path('', test_view, name='base'),
    path('products/<str:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/', ProductListView.as_view(), name='product_list'),
    # path('products/search', SearchView.as_view(), name='search_list'),
    # path(r'^list$', views.product_list),
]