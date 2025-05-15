from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ProductUnit, VerificationLog

class VerifyProductView(APIView):
    def get(self, request, serial_number):
        try:
            unit = ProductUnit.objects.get(serial_number=serial_number)
        except ProductUnit.DoesNotExist:
            return Response({
                "valid": False,
                "status": "Product not found. Please check the serial number."
            }, status=status.HTTP_404_NOT_FOUND)

        unit.verification_attempts += 1
        unit.save()

        ip = self.get_client_ip(request)

        if unit.verification_attempts <= 5:
            result = "Valid & Authentic"
        elif unit.verification_attempts <= 10:
            result = "Valid but Warning: Too Many Verifications"
        else:
            result = "Authentic but Blocked"

        VerificationLog.objects.create(
            product_unit=unit,
            ip_address=ip,
            result=result
        )

        return Response({
            "valid": True,
            "status": result,
            "attempts": unit.verification_attempts,
            "attempts_left": max(0, 10 - unit.verification_attempts)
        })

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')




#
# from django.views.decorators.csrf import csrf_exempt
#
# from django.views.decorators.http import require_GET
# from django.http import JsonResponse
# from .models import ProductUnit
# from django.shortcuts import get_object_or_404
#
# @require_GET
# def verify_product(request, serial_number):
#     unit = get_object_or_404(ProductUnit, serial_number=serial_number)
#
#     if unit.verification_attempts >= 5:
#         return JsonResponse({
#             "valid": True,
#             "status": "Verification limit reached. Please contact support."
#         }, status=403)
#
#     unit.verification_attempts += 1
#     unit.save()
#
#     if unit:
#         status = "Valid Product and Registered"
#     else:
#         valid=False
#         status = "Unauthorized Product"
#
#     return JsonResponse({
#         "valid": True,
#         "status": status,
#         "attempts_left": max(0, 5 - unit.verification_attempts)
#     })
#
#
#
# @csrf_exempt
# def register_product(request, serial_number):
#     if request.method == "POST":
#         unit = get_object_or_404(ProductUnit, serial_number=serial_number)
#         return JsonResponse({
#             "success": True,
#             "message": "Product registered successfully",
#
#         })
#     return JsonResponse({"error": "Invalid method"}, status=405)
#
