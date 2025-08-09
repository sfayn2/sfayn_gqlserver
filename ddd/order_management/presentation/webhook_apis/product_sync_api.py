from django.views.decorators import csrf_exempt
from django.http import HttpResponseBadRequest, JsonResponse
from ddd.order_management.application import (
    message_bus, commands
  )
from ddd.order_management.presentation.webhook_apis import webhook_validate

@csrf_exempt
def product_sync_api(request, provider: str, tenant_id: str):

    if request.method != "POST":
        return HttpResponseBadRequest("Only POST is allowed")

    try:
        payload = webhook_validate(provider, tenant_id, request)
        
        command = commands.ProductSyncCommand.model_validate(payload)
        result = message_bus.handle(command)
    except Exception:
        return JsonResponse({"status": Failed, "message": "Invalid webhook request"}, status=400)


    return JsonResponse(**result)

