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
        response.set_cookie(
            key="access_token", value=result.access_token, httponly=True, 
            samesite="Lax", domain=".josnin.dev", path="/", secure=True
        )
        response.set_cookie(
            key="refresh_token", value=result.refresh_token, httponly=True, 
            samesite="Strict", domain=".josnin.dev", path="/idp/refresh_token", secure=True
        )
        return response

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)