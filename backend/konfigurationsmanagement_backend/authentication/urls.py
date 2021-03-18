from django.urls import path

from . import AuthViews

app_name = 'authentication'

urlpatterns = [
    path('login/', AuthViews.login, name='login'),
    path('logout/', AuthViews.logout, name='logout'),
    path('register/', AuthViews.register, name='register'),
    path('userdata/', AuthViews.get_user, name='user_data')
]
