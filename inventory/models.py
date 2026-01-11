from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings # Para referenciar al usuario (Auth User)

# 1. CATEGORÍA (Recursiva)
class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=256, blank=True, null=True)
    # 'self' indica relación recursiva. null=True permite categorías raíz.
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subcategories')
    is_active = models.BooleanField(default=True)
    
    # Para auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='+')

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


# 2. MARCA
class Brand(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='+')

    def __str__(self):
        return self.name


# 3. PRODUCTO
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='products')
    
    sku = models.CharField(max_length=50, unique=True)
    upc = models.CharField(max_length=50, blank=True, null=True, verbose_name="Barcode/UPC")
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    
    # Precios (Decimal es vital para dinero)
    last_cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Logística
    weight = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True, help_text="kg")
    height = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, help_text="cm")
    width = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, help_text="cm")
    length = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, help_text="cm")
    
    min_stock_alert = models.PositiveIntegerField(default=5)
    
    # Campo flexible para atributos extra (Color, Talla, etc)
    properties = models.JSONField(blank=True, default=dict) 
    
    is_active = models.BooleanField(default=True)
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='+')

    def __str__(self):
        return f"{self.sku} - {self.name}"


# 4. BODEGA
class Warehouse(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='+')

    def __str__(self):
        return self.name


# 5. STOCK (Inventario Actual)
class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stocks')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='stocks')
    quantity = models.IntegerField(default=0)
    location = models.CharField(max_length=50, blank=True, null=True, help_text="Pasillo/Estante")
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # updated_by eliminado según diagrama final, se ve en Kardex

    class Meta:
        # Evita duplicados: Un producto solo puede tener UN registro por bodega
        unique_together = ('product', 'warehouse')
        verbose_name_plural = "Stocks"

    def __str__(self):
        return f"{self.product.sku} in {self.warehouse.name}: {self.quantity}"


# 6. KARDEX (Historial de Movimientos)
class Kardex(models.Model):

    # Definiendo el ENUM
    class MovementType(models.TextChoices):
        IN = 'IN', 'Entrada'
        OUT = 'OUT', 'Salida'
        # Podría agregar 'ADJUSTMENT', 'TRANSFER', etc.

    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='kardex_movements')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name='kardex_movements')
    
    type = models.CharField(max_length=10, choices=MovementType.choices)
    quantity = models.IntegerField(help_text="Valor absoluto de la cantidad movida")
    
    # Opcional: Balance después del movimiento (muy útil para reportes rápidos)
    # balance_after = models.IntegerField(null=True) 

    created_at = models.DateTimeField(auto_now_add=True) # Fecha transacción
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    class Meta:
        ordering = ['-created_at'] # Lo más reciente primero
        verbose_name_plural = "Kardex Entries"

    def __str__(self):
        return f"{self.type} {self.quantity} of {self.product.sku} at {self.warehouse.name}"