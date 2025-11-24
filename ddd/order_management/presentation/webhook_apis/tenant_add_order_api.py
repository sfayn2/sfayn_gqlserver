from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, JsonResponse
from ddd.order_management.application import (
    message_bus, commands
  )

@csrf_exempt
def tenant_add_order_api(request, tenant_id: str):

    if request.method != "POST":
        return HttpResponseBadRequest("Only POST is allowed")

    try:
        command = commands.PublishAddOrderCommand.model_validate(
            { "headers" : request.headers,
              "raw_body": request.body,
              "request_path": request.path,
              "tenant_id": tenant_id
            }
        )
        result = message_bus.handle(command)
        return JsonResponse(result.model_dump())
    except Exception as e:
        # TODO log exception
        return JsonResponse({"success": False, "message": str(e) }, status=500)



