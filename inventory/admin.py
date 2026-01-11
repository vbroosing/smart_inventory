from django.contrib import admin
from inventory.models import Category, Brand, Product, Warehouse, Stock, Kardex

# Register your models here.
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Warehouse)
admin.site.register(Stock)
admin.site.register(Kardex)    
# admin.site.register(Carga_familiar)
# admin.site.register(Contacto_emergencia)