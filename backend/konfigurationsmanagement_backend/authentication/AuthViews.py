import json

from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from .AuthenticationService import AuthenticationService


@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def login(request):
    try:
        json_data = json.loads(request.body)
        username = json_data["username"]
        password = json_data["password"]

        if username is None or password is None:
            return HttpResponseBadRequest('')

        token = auth_service.login(username, password)

        if token is None:
            return HttpResponseNotFound('')

        return JsonResponse({'token': token.key})
    except KeyError:
        return HttpResponseBadRequest('')


@csrf_exempt
@api_view(['POST'])
def logout(request):
    request.user.auth_token.delete()
    return HttpResponse('')


@api_view(['POST'])
@csrf_exempt
@permission_classes((AllowAny,))
def register(request):
    try:
        json_data = json.loads(request.body)
        username = json_data["username"]
        password = json_data["password"]

        if username is None or password is None:
            return HttpResponseBadRequest('')

        result = auth_service.register(username, password)

        if result:
            return HttpResponse("")
        else:
            return HttpResponseBadRequest('')
    except KeyError:
        return HttpResponseBadRequest('')


@api_view(['GET'])
@csrf_exempt
def get_user(request):
    user = request.user
    if user is not None:
        return JsonResponse(user.additionaluserinformation.as_json_detail())
    else:
        return HttpResponseBadRequest('')


auth_service = AuthenticationService()
