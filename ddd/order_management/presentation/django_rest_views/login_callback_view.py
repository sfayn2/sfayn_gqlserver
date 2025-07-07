import os
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseRedirect
from ddd.order_management.application import (
    message_bus, commands
  )

def login_callback_view(request):
    code = request.GET.get("code")
    redirect_uri = request.GET.get("redirect_uri")
    next_path = request.GET.get("next")

    try:
        command = commands.LoginCallbackCommand.model_validate({
            "code": code, 
            "redirect_uri": redirect_uri,
            "next_path": next_path
        })
        result = message_bus.handle(command)

        #response = JsonResponse(result.model_dump())
        response = HttpResponseRedirect(next)
        response.set_cookie(
            key="access_token", value=result.access_token, httponly=True, 
            samesite="Lax", domain=".mystore.com", path="/", secure=True
        )
        response.set_cookie(
            key="refresh_token", value=result.refresh_token, httponly=True, 
            samesite="Strict", domain=".mystore.com", path="/idp/refresh_token", secure=True
        )
        return response

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)