from django.urls import path

from . import RequirementGroupViews

app_name = 'configuration-management'

urlpatterns = [
    path('settings/', RequirementGroupViews.get_settings, name='settings'),
    path('settings/add/', RequirementGroupViews.add_setting, name='add_setting'),
    path('settings/delete/<int:id>/', RequirementGroupViews.delete_setting, name='delete_setting'),
    path('categorys/', RequirementGroupViews.get_categorys, name='categorys'),
    path('categorys/<int:id>/get_required_users/', RequirementGroupViews.get_required_users, name='get_required_users'),
    path('categorys/add/', RequirementGroupViews.add_category, name='add_categorys'),
    path('requirement_groups/', RequirementGroupViews.get_requirement_groups, name='get_requirement_groups'),
    path('requirement_groups/<int:id>/', RequirementGroupViews.get_requirement_group, name='get_requirement_group'),
    path('requirement_groups/add/', RequirementGroupViews.add_requirement_groups, name='add_requirement_groups'),
    path('requirement_groups/delete/<int:id>/', RequirementGroupViews.delete_requirement_groups, name='delete_requirement_groups'),
    path('requirement_groups/update/<int:id>/', RequirementGroupViews.update_requirement_groups, name='update_requirement_groups'),
    path('requirement_groups/<int:id>/add_comment/', RequirementGroupViews.add_user_comment, name='add_user_comment'),
    path('requirement_groups/category/<int:category_id>/', RequirementGroupViews.get_groups_by_category, name='get_groups_by_categorys'),
    path('category_requirement_groups/', RequirementGroupViews.get_category_requirement_groups, name='get_category_requirement_groups'),
    path('category_requirement_groups/<int:id>/', RequirementGroupViews.get_category_requirement_group, name='get_category_requirement_group'),
    path('category_requirement_groups/add/', RequirementGroupViews.add_category_requirement_group, name='add_category_requirement_groups'),
    path('category_requirement_groups/delete/<int:id>/', RequirementGroupViews.delete_category_requirement_groups, name='delete_category_requirement_groups'),
    path('category_requirement_groups/update/<int:id>/', RequirementGroupViews.update_category_requirement_groups, name='update_category_requirement_groups'),
    path('dashboard/<int:id>/', RequirementGroupViews.get_dashboard, name='get_dashboard')
]
