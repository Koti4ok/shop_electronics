from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Product(models.Model):
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100, default='', blank=True)
    category = models.CharField(max_length=100, default='', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(default='', blank=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, blank=True)

    # Характеристики для процесорів (CPU)
    cpu_cores = models.IntegerField(null=True, blank=True)
    cpu_threads = models.IntegerField(null=True, blank=True)
    cpu_frequency = models.CharField(max_length=50, default='', blank=True)

    # Характеристики для відеокарт (GPU)
    gpu_memory_size = models.IntegerField(null=True, blank=True)
    gpu_memory_type = models.CharField(max_length=50, default='', blank=True)

    # Характеристики для оперативки (RAM)
    ram_size = models.IntegerField(null=True, blank=True)
    ram_speed = models.CharField(max_length=50, default='', blank=True)

    # Характеристики для моніторів
    monitor_diagonal = models.CharField(max_length=50, default='', blank=True)
    monitor_hz = models.IntegerField(null=True, blank=True)
    monitor_panel = models.CharField(max_length=50, default='', blank=True)

    def __str__(self):
        return self.name

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"