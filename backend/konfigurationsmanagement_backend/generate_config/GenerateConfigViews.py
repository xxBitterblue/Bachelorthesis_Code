import json

from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .GenerateConfigService import GenerateConfigService


@csrf_exempt
@api_view(['POST'])
def create_config(request):
    try:
        json_data = json.loads(request.body)
        requirement_groups = json_data["requirement_groups"]

        config_path = generate_config_service.generate(requirement_groups)

        return JsonResponse({"path": config_path}, safe=False)
    except KeyError:
        return HttpResponseBadRequest('Value is missing')


generate_config_service = GenerateConfigService()