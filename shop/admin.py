from django.contrib import admin
from .models import Product, CartItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Поля, які будуть відображатися в таблиці всіх товарів
    list_display = ('name', 'brand', 'price', 'category')
    # Поля, за якими працюватиме пошуковий рядок вгорі
    search_fields = ('name', 'brand', 'category')
    # Справа з'явиться панель швидкої фільтрації
    list_filter = ('category', 'brand')

# Реєструємо також кошик, щоб адмін міг бачити сесії за потреби
admin.site.register(CartItem)