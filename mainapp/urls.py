""""""
from django.urls import path

from .views import test_view, ProductDetailView, ProductListView, CommentCreateView, UpdateCommentView, \
    DeleteCommentView

urlpatterns = [
    path('', test_view, name='base'),
    path('products/<str:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/<str:slug>/comment/', CommentCreateView.as_view(), name='comment_create'),
    path('products/<int:pk>/update', UpdateCommentView.as_view(), name='comment_update'),
    path('products/<int:pk>/delete', DeleteCommentView.as_view(), name='comment_delete'),
]