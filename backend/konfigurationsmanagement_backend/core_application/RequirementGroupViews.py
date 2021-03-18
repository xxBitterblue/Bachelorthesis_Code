import json

from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .RequirementGroupService import RequirementGroupService


@csrf_exempt
@api_view(['GET'])
def get_requirement_groups(request):
    requirement_groups = requirement_group_service.get_requirement_groups()
    return JsonResponse({
        "requirement_groups": [group.as_json() for group in requirement_groups]
    })

@csrf_exempt
@api_view(['GET'])
def get_requirement_group(request, id):
    requirement_group = requirement_group_service.get_requirement_group(id)
    return JsonResponse({
        "requirement_group": requirement_group.as_json()
    })

@csrf_exempt
@api_view(['GET'])
def get_groups_by_category(request, category_id):
    requirement_group, category_group = requirement_group_service.get_groups_by_category(category_id)
    json = {}
    json["requirement_group"] = [group.as_json() for group in requirement_group]
    json["category_requirement_group"] = [group.as_category_group_json() for group in category_group]
    return JsonResponse(json, safe=False)

@csrf_exempt
@api_view(['POST'])
def add_requirement_groups(request):
    try:
        json_data = json.loads(request.body)
        requirement_group_name = json_data["requirement_group_name"]
        status = json_data["status"]
        status_comment = json_data["status_comment"]
        author = request.user
        category = json_data["category"]
        software_list = json_data["software_list"]

        requirement_group = requirement_group_service.add_requirement_group(requirement_group_name, status, status_comment, author, category, software_list)

        if requirement_group is not None:
            return JsonResponse(requirement_group.as_json(), safe=False)
        else:
            return HttpResponseForbidden()
    except KeyError:
        return HttpResponseBadRequest('Value is missing')

@csrf_exempt
@api_view(['POST'])
def update_requirement_groups(request, id):
    try:
        json_data = json.loads(request.body)
        requirement_group_name = json_data["requirement_group_name"]
        status = json_data["status"]
        status_comment = json_data["status_comment"]
        author = request.user
        category = json_data["category"]
        software_list = json_data["software_list"]
        change_reason = json_data["change_reason"]

        requirement_group = requirement_group_service.update_requirement_group(id, requirement_group_name, status, status_comment, author, category, software_list, change_reason)

        if requirement_group is not None:
            return JsonResponse(requirement_group.as_json(), safe=False)
        else:
            return HttpResponseForbidden()

    except KeyError:
        return HttpResponseBadRequest('Value is missing')

@csrf_exempt
@api_view(['POST'])
def delete_requirement_groups(request, id):
    result = requirement_group_service.delete_requirement_group(id)
    return JsonResponse({"result": result})

@csrf_exempt
@api_view(['GET'])
def get_category_requirement_groups(request):
    category_requirement_groups = requirement_group_service.get_category_requirement_groups()
    return JsonResponse({
        "requirement_groups": [group.as_category_group_json() for group in category_requirement_groups]
    })

@csrf_exempt
@api_view(['GET'])
def get_category_requirement_group(request, id):
    category_requirement_groups = requirement_group_service.get_category_requirement_group(id)
    return JsonResponse({
        "requirement_groups": category_requirement_groups.as_category_group_json()
    })

@csrf_exempt
@api_view(['POST'])
def add_category_requirement_group(request):
    try:
        json_data = json.loads(request.body)
        category_requirement_group_name = json_data["requirement_group_name"]
        status = json_data["status"]
        status_comment = json_data["status_comment"]
        author = request.user
        category = json_data["category"]
        software_list = json_data["software_list"]
        reference_groups = json_data["reference_groups"]

        category_requirement_group = requirement_group_service.add_category_requirement_group(category_requirement_group_name, status, status_comment, author, category, software_list, reference_groups)

        if category_requirement_group is not None:
            return JsonResponse(category_requirement_group.as_category_group_json(), safe=False)
        else:
            return HttpResponseForbidden()
    except KeyError:
        return HttpResponseBadRequest('Value is missing')

@csrf_exempt
@api_view(['POST'])
def update_category_requirement_groups(request, id):
    try:
        json_data = json.loads(request.body)
        requirement_group_name = json_data["requirement_group_name"]
        status = json_data["status"]
        status_comment = json_data["status_comment"]
        author = request.user
        category = json_data["category"]
        software_list = json_data["software_list"]
        change_reason = json_data["change_reason"]
        reference_groups = json_data["reference_groups"]

        category_requirement_group = requirement_group_service.update_category_requirement_group(id, requirement_group_name, status, status_comment, author, category, software_list, change_reason, reference_groups)

        if category_requirement_group is not None:
            return JsonResponse(category_requirement_group.as_category_group_json(), safe=False)
        else:
            return HttpResponseForbidden()
    except KeyError:
        return HttpResponseBadRequest('Value is missing')

@csrf_exempt
@api_view(['POST'])
def delete_category_requirement_groups(request, id):
    result = requirement_group_service.delete_category_requirement_group(id)
    return JsonResponse({"result": result})


@csrf_exempt
@api_view(['POST'])
def add_user_comment(request, id):
    try:
        json_data = json.loads(request.body)
        comment_text = json_data["comment_text"]
        author = request.user

        result = requirement_group_service.add_user_comment(id, author, comment_text)

        return JsonResponse({"result": result})
    except KeyError:
        return HttpResponseBadRequest('Value is missing')


@csrf_exempt
@api_view(['GET'])
def get_settings(request):
    settings_list = requirement_group_service.get_all_settings()
    return JsonResponse({
        "settings": [setting.as_json() for setting in settings_list]
    })


@csrf_exempt
@api_view(['POST'])
def add_setting(request):
    try:
        json_data = json.loads(request.body)
        deadline = json_data["deadline"]
        author = request.user
        required_users = json_data["required_users"]
        categorys = json_data["categorys"]

        setting = requirement_group_service.add_setting(deadline, author, required_users, categorys)

        return JsonResponse(setting.as_json(), safe=False)
    except KeyError:
        return HttpResponseBadRequest('Value is missing')


@csrf_exempt
@api_view(['DELETE'])
def delete_setting(request, id):
    result = requirement_group_service.delete_setting(id)
    return JsonResponse({"result": result})


@csrf_exempt
@api_view(['GET'])
def get_categorys(request):
    category_list = requirement_group_service.get_all_categorys()
    return JsonResponse({
        "categorys": [category.as_json() for category in category_list]
    })

@csrf_exempt
@api_view(['GET'])
def get_required_users(request, id):
    user_list = requirement_group_service.get_required_users(id)
    return JsonResponse({
        "user_list": [user.additionaluserinformation.as_json() for user in user_list]
    })

@csrf_exempt
@api_view(['POST'])
def add_category(request):
    try:
        json_data = json.loads(request.body)
        category_name = json_data["category_name"]
        parent = json_data["parent"]

        category = requirement_group_service.add_category(category_name, parent)

        return JsonResponse(category.as_json(), safe=False)
    except KeyError:
        return HttpResponseBadRequest('Value is missing')

@csrf_exempt
@api_view(['GET'])
def get_dashboard(request, id):
    dashboard = requirement_group_service.get_dashboard(id)

    return JsonResponse({'dashboard': [entry.as_json() for entry in dashboard.all()]}, safe=False)


requirement_group_service = RequirementGroupService()
