import os
from django.http import JsonResponse, HttpResponseBadRequest
from ddd.order_management.application import (
    message_bus, commands
  )

def login_callback_view(request):
    code = request.GET.get("code")
    redirect_uri = request.build_absolute_uri(request.path)

    if not code:
        return HttpResponseBadRequest("Missing authorization code.")
    
    try:
        command = commands.LoginCallbackCommand.model_validate({"code":code, "redirect_uri": redirect_uri})
        result = message_bus.handle(command)

        response = JsonResponse(result.model_dump())
        response.set_cookie("access_token", result.access_token, httponly=True, samesite="Lax")
        return response

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)