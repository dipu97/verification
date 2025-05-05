from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import ProductUnit
from django.views.decorators.csrf import csrf_exempt

def verify_product(request, serial_number):
    unit = get_object_or_404(ProductUnit, serial_number=serial_number)

    if unit:
        status = "Valid Product and Registered"
        valid = True
    else:
        status = "Invalid Product"
        valid = False

    return JsonResponse({
        "valid": valid,
        "status": status,
    })


@csrf_exempt
def register_product(request, serial_number):
    if request.method == "POST":
        unit = get_object_or_404(ProductUnit, serial_number=serial_number)
        if unit.is_registered:
            return JsonResponse({"success": False, "message": "Already registered"}, status=400)
        unit.is_registered = True
        unit.save()
        return JsonResponse({"success": True, "message": "Product registered successfully"})

    return JsonResponse({"error": "Invalid method"}, status=405)
