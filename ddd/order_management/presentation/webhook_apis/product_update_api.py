from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, JsonResponse
from ddd.order_management.application import (
    message_bus, commands
  )
from ddd.order_management.presentation.webhook_apis import common

@csrf_exempt
def product_update_api(request, provider: str, tenant_id: str):

    if request.method != "POST":
        return HttpResponseBadRequest("Only POST is allowed")

    try:
        payload = common.validate_webhook(provider, tenant_id, request)
        
        command = commands.PublishProductUpdateCommand.model_validate(payload)
        result = message_bus.handle(command)
        return JsonResponse(result.model_dump())
    except Exception as e:
        # TODO log exception
        return JsonResponse({"success": False, "message": "Invalid webhook request"}, status=500)



