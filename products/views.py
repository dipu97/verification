
from django.views.decorators.csrf import csrf_exempt

from django.views.decorators.http import require_GET
from django.http import JsonResponse
from .models import ProductUnit
from django.shortcuts import get_object_or_404

@require_GET
def verify_product(request, serial_number):
    unit = get_object_or_404(ProductUnit, serial_number=serial_number)

    if unit.verification_attempts >= 5:
        return JsonResponse({
            "valid": False,
            "status": "Verification limit reached. Please contact support."
        }, status=403)

    unit.verification_attempts += 1
    unit.save()

    if unit:
        status = "Valid Product and Registered"
    else:
        status = "Unauthorized Product"

    return JsonResponse({
        "valid": True,
        "status": status,
        "attempts_left": max(0, 5 - unit.verification_attempts)
    })



@csrf_exempt
def register_product(request, serial_number):
    if request.method == "POST":
        unit = get_object_or_404(ProductUnit, serial_number=serial_number)
        return JsonResponse({
            "success": True,
            "message": "Product registered successfully",

        })
    return JsonResponse({"error": "Invalid method"}, status=405)

