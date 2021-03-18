from django.urls import path

from . import ValidationViews

app_name = 'validation'

urlpatterns = [
    path('', ValidationViews.get_all, name='get_all_validations'),
    path('<int:id>/', ValidationViews.get_rule, name='get_validation_rule'),
    path('add/', ValidationViews.add_rule, name='add_validation_rule'),
    path('delete/<int:id>/', ValidationViews.delete_rule, name='delete_validation_rule'),
    path('update/<int:id>/', ValidationViews.update_rule, name='update_validation_rule'),
    path('validate_group/', ValidationViews.validate_group, name='validate_group'),
    path('validation_structure/', ValidationViews.get_validation_structure, name='get_validate_structure')
]
