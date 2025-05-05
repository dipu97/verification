from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product, ProductUnit
import uuid

@receiver(post_save, sender=Product)
def generate_product_units(sender, instance, created, **kwargs):
    existing = instance.units.count()
    to_create = instance.stock_count - existing
    if to_create > 0:
        units = []
        for _ in range(to_create):
            unit = ProductUnit(product=instance)
            unit.serial_number = f"{instance.id}-{uuid.uuid4().hex[:10].upper()}"
            units.append(unit)
        ProductUnit.objects.bulk_create(units)

