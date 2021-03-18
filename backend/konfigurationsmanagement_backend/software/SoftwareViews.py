import json

from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .SoftwareService import SoftwareService


@csrf_exempt
@api_view(['GET'])
def get_all(request):
    software_list = software_service.get_all()
    return JsonResponse({
        "software": [software.as_json() for software in software_list]
    })


@csrf_exempt
@api_view(['POST'])
def add(request):
    try:
        json_data = json.loads(request.body)
        name = json_data["name"]
        version = json_data["version"]
        type = json_data["type"]
        dependency_software = json_data["dependency_software"]

        software = software_service.add(name, version, type, dependency_software)

        return JsonResponse(software.as_json(), safe=False)
    except KeyError:
        return HttpResponseBadRequest('Value is missing')


@csrf_exempt
@api_view(['DELETE'])
def delete(request, id):
    result = software_service.delete(id)
    return JsonResponse({"result": result})


@csrf_exempt
@api_view(['POST'])
def update(request, id):
    try:
        json_data = json.loads(request.body)
        name = json_data["name"]
        version = json_data["version"]
        type = json_data["type"]
        dependency_software = json_data["dependency_software"]

        software = software_service.update(id, name, version, type, dependency_software)

        return JsonResponse(software.as_json(), safe=False)
    except KeyError:
        return HttpResponseBadRequest('Value is missing')


software_service = SoftwareService()
