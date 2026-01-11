from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Kardex, Stock

@receiver(post_save, sender=Kardex)
def update_stock_on_kardex_entry(sender, instance, created, **kwargs):
    """
    Se ejecuta automáticamente CADA VEZ que se crea una fila en Kardex.
    Actualiza la cantidad en el modelo Stock.
    """
    if created:  # Solo si es un registro nuevo (no al editar)
        # 1. Buscamos el stock existente o lo creamos en 0 si no existe
        stock, _ = Stock.objects.get_or_create(
            product=instance.product,
            warehouse=instance.warehouse,
            defaults={'quantity': 0}
        )

        # 2. Aplicamos la lógica matemática
        if instance.type == Kardex.MovementType.IN:
            stock.quantity += instance.quantity
        elif instance.type == Kardex.MovementType.OUT:
            stock.quantity -= instance.quantity
        
        # 3. Guardamos el nuevo total
        stock.save()