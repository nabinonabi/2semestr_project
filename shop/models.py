from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, RegexValidator
from django.core.exceptions import ValidationError



class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(blank=True, null=True, verbose_name="Описание товара")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория товара"
        verbose_name_plural = "Категории товаров"

class Proizvodstvo(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    country = models.CharField(max_length=100, verbose_name="Страна производства")
    description = models.TextField(max_length=100, verbose_name="Описание") 

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"  

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name="Цена")
    stock_quantity = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Количество товаров на складе")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    proizvodstvo = models.ForeignKey(Proizvodstvo, on_delete=models.CASCADE, verbose_name="Производство")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

class Cart(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    create_add = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Корзина {self.user.username}"

    def total_price(self):
        return sum(item.item_price() for item in self.items.all())

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"  

class CartItem(models.Model): 
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name="Корзина")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(verbose_name="Количество")    

    def __str__(self):
        return f"{self.product.name} ({self.quantity} шт.)"

    def item_price(self):
        return self.product.price * self.quantity

    def clean(self):
        if self.quantity > self.product.stock_quantity:
            raise ValidationError(
                f"Количество ({self.quantity}) превышает наличие на складе ({self.product.stock_quantity})"
            )
    
    def save(self, *args, **kwargs):
        self.full_clean()  
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Элемент корзины"
        verbose_name_plural = "Элементы корзины"

belarus_phone_validator = RegexValidator(
    regex=r'^\+375\d{9}$',
    message="Номер телефона должен быть в формате +375XXXXXXXXX (всего 12 символов, без пробелов)."
)

class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('paid', 'Оплачен'),
        ('shipped', 'Отправлен'),
        ('completed', 'Завершен'),
        ('cancelled', 'Отменен'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(
        max_length=20, 
        validators=[belarus_phone_validator], 
        verbose_name="Телефон",
        help_text="Формат: +375XXXXXXXXX"
    )
    address = models.TextField(verbose_name="Адрес доставки")
    comments = models.TextField(blank=True, null=True, verbose_name="Комментарий")
    
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Общая сумма")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус")
    
    def __str__(self):
        return f"Заказ #{self.id} от {self.user.username}"
    
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created_at']

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    
    def __str__(self):
        return f"{self.product.name} ({self.quantity} шт.)"
    
    def get_total(self):
        return self.price * self.quantity
    
    class Meta:
        verbose_name = "Элемент заказа"
        verbose_name_plural = "Элементы заказа"

class Profile(models.Model):
    class Roles(models.TextChoices):
        CUSTOMER = 'CUSTOMER', 'Покупатель'
        MANAGER = 'MANAGER', 'Менеджер'
        ADMIN = 'ADMIN', 'Администратор'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name="Пользователь")
    role = models.CharField(max_length=10, choices=Roles.choices, default=Roles.CUSTOMER, verbose_name="Роль")
    full_name = models.CharField(max_length=255, blank=True, verbose_name="ФИО")
    phone = models.CharField(
        max_length=20, 
        blank=True, 
        validators=[belarus_phone_validator], 
        verbose_name="Телефон",
        help_text="Формат: +375XXXXXXXXX"
    )
    address = models.TextField(blank=True, verbose_name="Адрес доставки")
    delivery_city = models.CharField(max_length=100, blank=True, verbose_name="Город доставки")
    favorite_category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name="Любимая категория"
    )

    def __str__(self):
        return f"Профиль: {self.user.username} ({self.get_role_display()})"

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()

