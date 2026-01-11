from django.contrib import admin
from .models import Category, Brand, Product, Warehouse, Stock, Kardex

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('sku', 'name', 'brand', 'category', 'selling_price', 'is_active')
    search_fields = ('sku', 'name', 'brand__name') # Permite buscar por nombre de marca
    list_filter = ('brand', 'category', 'is_active')

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('product', 'warehouse', 'quantity')
    list_filter = ('warehouse',)

@admin.register(Kardex)
class KardexAdmin(admin.ModelAdmin):
    list_display = ('product', 'warehouse', 'type', 'quantity', 'created_at', 'created_by')
    list_filter = ('type', 'warehouse', 'created_at')
    
    # Mantenemos created_at como readonly siempre
    readonly_fields = ('created_at', 'created_by')

    def save_model(self, request, obj, form, change):
        """
        Este método se ejecuta ANTES de guardar en la base de datos.
        Aquí inyectamos el usuario logueado automáticamente.
        """
        obj.created_by = request.user
        
        super().save_model(request, obj, form, change)

# Registro simple para los demás
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Warehouse)