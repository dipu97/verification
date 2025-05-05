from django.urls import path
from .views import verify_product, register_product

urlpatterns = [
    path('verify/<str:serial_number>/', verify_product, name='verify-product'),
    path('verify/<str:serial_number>/register/', register_product, name='register-product'),
]
