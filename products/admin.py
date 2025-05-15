# admin.py

import csv
from django.http import HttpResponse
from django.contrib import admin
from .models import Product, ProductUnit, VerificationLog


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'stock_count']
    actions = ['download_qr_codes_csv']

    def download_qr_codes_csv(self, request, queryset):
        # Create the response with CSV content type
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="qr_codes.csv"'

        writer = csv.writer(response)
        writer.writerow(['Product', 'Serial Number', 'QR Code URL', 'QR Code Image'])  # Column headers

        for product in queryset:
            # Retrieve all units for the selected product
            units = product.units.all()

            for unit in units:
                # QR code URL where image is hosted
                qr_code_url = unit.qr_code.url if unit.qr_code else ''
                qr_code_image_url = f"https://yourdomain.com{qr_code_url}" if qr_code_url else ''

                writer.writerow([product.name, unit.serial_number, qr_code_url, qr_code_image_url])

        return response

    download_qr_codes_csv.short_description = "Download QR Codes as CSV"

admin.site.register(ProductUnit)
admin.site.register(VerificationLog)