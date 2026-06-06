from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, CartItem
from .forms import ProductForm
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout


# ========================================================
# 1. ГОЛОВНА СТОРІНКА ТА ФІЛЬТРАЦІЯ
# ========================================================

def home(request):
    """Головна сторінка з пошуком, фільтрами та сортуванням заліза"""
    products = Product.objects.all()

    # Пошук по назві та бренду
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(Q(name__icontains=search_query) | Q(brand__icontains=search_query))

    # Фільтрація за категоріями та брендами
    current_category = request.GET.get('category', '')
    current_brand = request.GET.get('brand', '')

    if current_category:
        products = products.filter(category=current_category)
    if current_brand:
        products = products.filter(brand__iexact=current_brand.replace('_', ' '))

    # Сортування (Новинки, Дешевші, Дорожчі)
    current_sort = request.GET.get('sort', 'newest')
    if current_sort == 'price_low':
        products = products.order_by('price')
    elif current_sort == 'price_high':
        products = products.order_by('-price')
    else:  # newest
        products = products.order_by('-created_at')

    # Дані категорій для бічної панелі (Sidebar)
    categories_data = [
        {'code': 'cpu', 'name': 'Процесори (CPU)', 'brands': ['Intel', 'AMD']},
        {'code': 'gpu', 'name': 'Відеокарти (GPU)', 'brands': ['NVIDIA', 'AMD', 'ASUS', 'MSI', 'Gigabyte', 'Sapphire']},
        {'code': 'monitor', 'name': 'Монітори', 'brands': ['Samsung', 'LG', 'ASUS', 'MSI', 'Acer', 'AOC']},
        {'code': 'ram', 'name': 'Оперативна пам\'ять',
         'brands': ['Kingston FURY', 'G.Skill', 'Corsair', 'Crucial', 'Team Group']},
    ]

    # Підрахунок кількості товарів у кошику для іконки
    if request.user.is_authenticated:
        cart_count = CartItem.objects.filter(user=request.user).count()
    else:
        cart_count = CartItem.objects.filter(user=None).count()

    context = {
        'products': products,
        'search_query': search_query,
        'current_category': current_category,
        'current_brand': current_brand,
        'current_sort': current_sort,
        'categories_data': categories_data,
        'cart_count': cart_count,
    }
    return render(request, 'index.html', context)


# ========================================================
# 2. КЕРУВАННЯ ТОВАРАМИ (Додавання, Перегляд, Зміна)
# ========================================================

def product_detail(request, product_id):
    """Детальна сторінка конкретного товару (якщо є в урлах)"""
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})


def add_product(request):
    """Додавання нового товару через форму"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProductForm()
    return render(request, 'add.html', {'form': form})


def edit_product(request, product_id):
    """Редагування існуючого товару"""
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProductForm(instance=product)
    return render(request, 'add.html', {'form': form, 'product': product})


def delete_product(request, product_id):
    """Видалення товару"""
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('home')


# ========================================================
# 3. ЛОГІКА КОШИКА
# ========================================================

def cart_detail(request):
    """Відображення сторінки кошика"""
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        cart_items = CartItem.objects.filter(user=None)

    total_price = sum(item.product.price * item.quantity for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'cart.html', context)


def add_to_cart(request, product_id):
    """Додавання товару в кошик"""
    product = get_object_or_404(Product, id=product_id)
    user = request.user if request.user.is_authenticated else None

    cart_item, created = CartItem.objects.get_or_create(product=product, user=user)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_detail')


def remove_from_cart(request, item_id):
    """Видалення однієї позиції з кошика"""
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('cart_detail')


def clear_cart(request):
    """Повне очищення кошика"""
    if request.user.is_authenticated:
        CartItem.objects.filter(user=request.user).delete()
    else:
        CartItem.objects.filter(user=None).delete()
    return redirect('cart_detail')


# ========================================================
# 4. ЛОГІКА ПОРІВНЯННЯ ТОВАРІВ (Челендж пофікшено тут)
# ========================================================

def compare_detail(request):
    """Сторінка порівняння характеристик заліза"""
    compare_ids = request.session.get('compare_list', [])
    products = Product.objects.filter(id__in=compare_ids)
    return render(request, 'compare.html', {'products': products})


def add_to_compare(request, product_id):
    """Додавання товару до списку порівняння"""
    compare_list = request.session.get('compare_list', [])
    if product_id not in compare_list:
        compare_list.append(product_id)
        request.session['compare_list'] = compare_list
    return redirect('compare_detail')


def remove_from_compare(request, product_id):
    """Видалення товару зі списку порівняння"""
    compare_list = request.session.get('compare_list', [])
    if product_id in compare_list:
        compare_list.remove(product_id)
        request.session['compare_list'] = compare_list
    return redirect('compare_detail')


def clear_compare(request):
    """Очищення всього списку порівняння"""
    if 'compare_list' in request.session:
        del request.session['compare_list']
    return redirect('compare_detail')


# ========================================================
# 5. СИСТЕМА АВТОРИЗАЦІЇ ТА РЕЄСТРАЦІЇ
# ========================================================

def register_view(request):
    """Реєстрація нового користувача"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    """Вхід в акаунт"""
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    """Вихід з акаунту"""
    logout(request)
    return redirect('home')