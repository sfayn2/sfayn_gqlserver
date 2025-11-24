from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, JsonResponse
from ddd.order_management.application import (
    message_bus, commands
  )
#from ddd.order_management.infrastructure import (
#    webhook_receiver
#)

@csrf_exempt
def shipment_updates_api(request):

    if request.method != "POST":
        return HttpResponseBadRequest("Only POST is allowed")

    try:
        ##TODO how to get tenant upfront
        #temp_payload = json.loads(request.body.decode('utf-8')) 
        #tenant_id = temp_payload["results"]["metadata"]["tenant_id"]
        #payload = webhook_receiver.WebhookReceiverService.validate(
        #        tenant_id, 
        #        request
        #    )
        
        command = commands.PublishShipmentUpdatesCommand.model_validate(
            { "headers" : request.headers,
              "raw_body": request.body,
              "request_path": request.path
            }
        )
        result = message_bus.handle(command)
        return JsonResponse(result.model_dump())
    except Exception as e:
        # TODO log exception
        return JsonResponse({"success": False, "message": str(e) }, status=500)



