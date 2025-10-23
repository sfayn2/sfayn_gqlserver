from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, JsonResponse
from ddd.order_management.application import (
    message_bus, commands
  )
from ddd.order_management.application.services import WebhookValidationService

@csrf_exempt
def tenant_workflow_update_api(request, tenant_id: str):

    if request.method != "POST":
        return HttpResponseBadRequest("Only POST is allowed")

    try:
        payload = WebhookValidationService.validate(
                tenant_id, 
                request
            )
        
        command = commands.PublishTenantWorkflowUpdateCommand.model_validate(payload)
        result = message_bus.handle(command)
        return JsonResponse(result.model_dump())
    except Exception as e:
        # TODO log exception
        return JsonResponse({"success": False, "message": str(e) }, status=500)



