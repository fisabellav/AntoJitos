from django.urls import path
from crud import views

urlpatterns = [
    path ('product-list/', views.product_list, name='product-list'),
    path ('order-list/', views.order_list, name='order-list'),
    path ('add-product/', views.add_product, name='add-product'),
    path('product-list/delete/<id>', views.productlist_delete, name='productlist-delete'),
    path('product-list/edit/<id>', views.productlist_edit, name='productlist-edit'),
    path('product-list/detail/<id>', views.product_detail, name='product-detail'),
    path('crud/filter-by-category/<str:category>/', views.filter_by_category, name='filter-by-category'),
    path('crud/filter-by-flavor/<str:flavor>/', views.filter_by_flavor, name='filter-by-flavor'),
]