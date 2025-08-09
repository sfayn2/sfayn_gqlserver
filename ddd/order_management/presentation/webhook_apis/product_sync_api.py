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
        
        command = commands.PublishProductUpdateCommand.model_validate(payload)
        result = message_bus.handle(command)
        return JsonResponse(result, status=200)
    except Exception:
        return JsonResponse({"message": "Invalid webhook request"}, status=500)



