from django.urls import path

from . import GenerateConfigViews

app_name = 'generate_config'

urlpatterns = [
    path('', GenerateConfigViews.create_config, name='get_all_validations')
]
