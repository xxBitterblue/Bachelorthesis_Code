import json

from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .ValidationService import ValidationService

@csrf_exempt
@api_view(['GET'])
def get_all(request):
    validation_rules = validation_service.get_all()
    return JsonResponse({
        "validation_rules": [rule.as_json() for rule in validation_rules]
    })

@csrf_exempt
@api_view(['GET'])
def get_rule(request, id):
    validation_rule = validation_service.get_rule(id)
    return JsonResponse({
        "validation_rule": validation_rule.as_json()
    })

@csrf_exempt
@api_view(['POST'])
def add_rule(request):
    try:
        json_data = json.loads(request.body)
        name = json_data["name"]
        active = json_data["active"]
        is_global = json_data["is_global"]
        rule = json_data["rule"]
        categorys = json_data["categorys"]
        author = request.user

        validation_rule = validation_service.add_rule(name, active, is_global, rule, categorys, author)

        return JsonResponse(validation_rule.as_json(), safe=False)
    except KeyError:
        return HttpResponseBadRequest('Value is missing')

@csrf_exempt
@api_view(['POST'])
def delete_rule(request, id):
    result = validation_service.delete(id)
    return JsonResponse({"result": result})

@csrf_exempt
@api_view(['POST'])
def update_rule(request, id):
    try:
        json_data = json.loads(request.body)
        name = json_data["name"]
        active = json_data["active"]
        is_global = json_data["is_global"]
        rule = json_data["rule"]
        categorys = json_data["categorys"]

        validation_rule = validation_service.update(id, name, active, is_global, rule, categorys)

        return JsonResponse(validation_rule.as_json(), safe=False)
    except KeyError:
        return HttpResponseBadRequest('Value is missing')

@csrf_exempt
@api_view(['POST'])
def validate_group(request):
    try:
        json_data = json.loads(request.body)
        software_list = json_data["software_list"]

        if "category" in json_data:
            category = json_data["category"]
        else:
            category = None

        validation_service.validate_group(software_list, category)

        return HttpResponse("")
    except KeyError:
        return HttpResponseBadRequest('Value is missing')

@csrf_exempt
@api_view(['GET'])
def get_validation_structure(request):
    example_software, exception_options = validation_service.get_validation_structure()

    return JsonResponse({"software_structure": {"software_list": [software.as_example_json() for software in example_software]}, "exception_options": exception_options}, safe=False)


validation_service = ValidationService()
