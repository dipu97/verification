import uuid
import qrcode
from io import BytesIO
from django.core.files import File
from django.db import models
from django.contrib.auth import get_user_model
User=get_user_model()

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    stock_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class ProductUnit(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="units")
    serial_number = models.CharField(max_length=100, unique=True, blank=False, null=False)
    is_registered = models.BooleanField(default=False)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)
    verification_attempts = models.PositiveIntegerField(default=0)  # New field

    def save(self, *args, **kwargs):
        if not self.serial_number:
            self.serial_number = f"{self.product.id}-{uuid.uuid4().hex[:10].upper()}"

        if not self.qr_code:
            verify_url = f"https://yourdomain.com/verify/{self.serial_number}/"
            qr_img = qrcode.make(verify_url)
            buffer = BytesIO()
            qr_img.save(buffer, format='PNG')
            self.qr_code.save(f'{self.serial_number}.png', File(buffer), save=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.serial_number



