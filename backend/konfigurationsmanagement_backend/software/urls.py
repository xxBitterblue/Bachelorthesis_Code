from django.urls import path

from . import SoftwareViews

app_name = 'software'

urlpatterns = [
    path('', SoftwareViews.get_all, name='getAll'),
    path('add/', SoftwareViews.add, name='add'),
    path('delete/<int:id>/', SoftwareViews.delete, name='delete'),
    path('update/<int:id>/', SoftwareViews.update, name='update')
]
