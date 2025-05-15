from django.urls import path
from .views import VerifyProductView

urlpatterns = [
    path('verify/<str:serial_number>/', VerifyProductView.as_view(), name='verify-product'),
]
