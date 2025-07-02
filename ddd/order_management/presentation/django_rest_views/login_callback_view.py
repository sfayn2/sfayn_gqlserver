import os
from django.http import JsonResponse, HttpResponseBadRequest
from ddd.order_management.application import (
    message_bus, commands
  )

def login_callback_view(request):
    code = request.GET.get("code")
    redirect_uri = request.GET.get("redirect_uri")

    if not code or not redirect_uri:
        return HttpResponseBadRequest("Missing authorization code or redirect_uri.")
    
    try:
        command = commands.LoginCallbackCommand.model_validate({
            "code": code, 
            "redirect_uri": redirect_uri
        })
        result = message_bus.handle(command)

        response = JsonResponse(result.model_dump())
        response.set_cookie("access_token", result.access_token, httponly=True, samesite="Lax")
        return response

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)