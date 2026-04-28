from django.contrib import admin
from .models import Category, Proizvodstvo, Product, Cart, CartItem
from .models import Order, OrderItem



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']



@admin.register(Proizvodstvo)
class ProizvodstvoAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock_quantity', 'category', 'proizvodstvo']
    list_filter = ['category', 'proizvodstvo']
    search_fields = ['name', 'description']
    list_editable = ['price', 'stock_quantity']



@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'id']  
    search_fields = ['user__username']



@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity']
    list_filter = ['cart']
    search_fields = ['product__name']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name', 'last_name', 'total_price', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'first_name', 'last_name', 'email']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price', 'get_total']
    list_filter = ['order']
    
    def get_total(self, obj):
        return obj.get_total()
    get_total.short_description = 'Сумма'