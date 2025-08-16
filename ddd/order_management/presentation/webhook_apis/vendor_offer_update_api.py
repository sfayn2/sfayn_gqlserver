from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, JsonResponse
from ddd.order_management.application import (
    message_bus, commands
  )
from ddd.order_management.application.services import validate_webhook

@csrf_exempt
def vendor_offer_update_api(request, provider: str, tenant_id: str):

    if request.method != "POST":
        return HttpResponseBadRequest("Only POST is allowed")

    try:
        payload = validate_webhook(
                provider, 
                tenant_id, 
                request
            )
        
        command = commands.PublishVendorOfferUpdateCommand.model_validate(payload)
        result = message_bus.handle(command)
        return JsonResponse(result.model_dump())
    except Exception as e:
        # TODO log exception
        return JsonResponse({"success": False, "message": str(e) }, status=500)



