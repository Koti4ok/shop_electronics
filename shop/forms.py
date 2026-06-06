from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'category', 'brand', 'name', 'price', 'image', 'description',
            'cpu_frequency', 'cpu_cores', 'cpu_threads',
            'gpu_memory_size', 'gpu_memory_type',
            'monitor_hz', 'monitor_diagonal', 'monitor_panel',
            'ram_size', 'ram_speed'
        ]