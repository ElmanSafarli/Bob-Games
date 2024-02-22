from django.urls import path
from .views import HomePage, ProductListView, ProductDetailView, CategoryProductListView, cart_view, add_to_cart, remove_from_cart, checkout, send_to_telegram_view, SubcategoryProductListView

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('products/', ProductListView.as_view(), name='products-list'),
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('category/<slug:category_slug>/', CategoryProductListView.as_view(), name='category_products'),
    path('subcategory/<slug:subcategory_slug>/', SubcategoryProductListView.as_view(), name='subcategory_products'),
    path('cart/', cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout, name='checkout'),
    path('send-to-telegram/', send_to_telegram_view, name='send_to_telegram'),
]
