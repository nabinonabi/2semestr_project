from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'shop'

router = DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'proizvodstvos', views.ProizvodstvoViewSet)
router.register(r'carts', views.CartViewSet)
router.register(r'cart-items', views.CartItemViewSet)
router.register(r'orders', views.OrderViewSet, basename='order')

urlpatterns = [
    path('', views.index, name='index'),
    path('author/', views.author_page, name='author'),
    path('shop-info/', views.shop_info_page, name='shop_info'),
    path('catalog/', views.product_list, name='product_list'),
    path('catalog/<int:pk>/', views.product_detail, name='product_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('checkout/', views.checkout, name='checkout'),
    
    
    path('profile/', TemplateView.as_view(template_name='shop/profile.html'), name='profile_page'),
    path('api/me/', views.api_me, name='api_me'),
    path('api/', include(router.urls)),
]
