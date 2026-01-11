# from django.contrib import admin
# from .models import Category, Brand, Product, Warehouse, Stock, Kardex

# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('sku', 'name', 'brand', 'category', 'selling_price', 'is_active')
#     search_fields = ('sku', 'name', 'brand__name') # Permite buscar por nombre de marca
#     list_filter = ('brand', 'category', 'is_active')

# @admin.register(Stock)
# class StockAdmin(admin.ModelAdmin):
#     list_display = ('product', 'warehouse', 'quantity')
#     list_filter = ('warehouse',)

from django.contrib import admin
from inventory.models import Category, Brand, Product, Warehouse, Stock, Kardex

# Configuraciones personalizadas para los modelos clave

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('sku', 'name', 'brand', 'category', 'selling_price', 'is_active')
    search_fields = ('sku', 'name', 'brand__name')
    list_filter = ('brand', 'category', 'is_active')

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('product', 'warehouse', 'quantity')
    list_filter = ('warehouse',)

@admin.register(Kardex)
class KardexAdmin(admin.ModelAdmin):
    list_display = ('product', 'warehouse', 'type', 'quantity', 'created_at', 'created_by')
    list_filter = ('type', 'warehouse', 'created_at')
    # Ocultamos created_by del formulario para que no moleste, total se llena solo
    exclude = ('created_by',) 
    readonly_fields = ('created_at',)

    def save_model(self, request, obj, form, change):
        # El parámetro 'change' es False si se está CREANDO, True si se está EDITANDO
        if not change: 
            obj.created_by = request.user
        
        super().save_model(request, obj, form, change)

# Registros simples para los catálogos
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Warehouse)