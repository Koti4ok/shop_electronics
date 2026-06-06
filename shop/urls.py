from django.urls import path
from . import views

urlpatterns = [
    # Головна та кошик
    path("", views.home, name="home"),
    path("cart/", views.cart_detail, name="cart_detail"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/clear/", views.clear_cart, name="clear_cart"),

    # Авторизація
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Порівняння
    path("compare/", views.compare_detail, name="compare_detail"),
    path("compare/add/<int:product_id>/", views.add_to_compare, name="add_to_compare"),

    # Адмін-панель керування товарами
    path("product/add/", views.add_product, name="add_product"),
    path("product/edit/<int:product_id>/", views.edit_product, name="edit_product"), # Новий маршрут!
]