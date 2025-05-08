from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import ProductUnit

from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now

@csrf_exempt
def verify_product(request, serial_number):
    code = request.GET.get('code')
    unit = get_object_or_404(ProductUnit, serial_number=serial_number)

    if str(unit.secret_code) != str(code):
        return JsonResponse({"valid": False, "status": "Invalid secret code"}, status=403)

    if unit.usage_count >= unit.max_uses:
        return JsonResponse({"valid": False, "status": "Code usage limit exceeded"}, status=403)

    # Mark one more use
    unit.usage_count += 1
    unit.save()

    return JsonResponse({
        "valid": True,
        "status": f"Product is valid. Remaining uses: {unit.max_uses - unit.usage_count}"
    })



@csrf_exempt
def register_product(request, serial_number):
    if request.method == "POST":
        unit = get_object_or_404(ProductUnit, serial_number=serial_number)
        if unit.is_registered:
            return JsonResponse({"success": False, "message": "Already registered"}, status=400)
        unit.is_registered = True
        unit.save()
        return JsonResponse({
            "success": True,
            "message": "Product registered successfully",
            "secret_code": str(unit.secret_code)
        })
    return JsonResponse({"error": "Invalid method"}, status=405)

