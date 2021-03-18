from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from authentication.models import AdditionalUserInformation
from authentication.models import Role


class AuthenticationService:

    def login(self, username, password):
        user = authenticate(username=username, password=password)

        if not user:
            return None

        token, _ = Token.objects.get_or_create(user=user)

        return token

    def register(self, username, password):
        user = User.objects.create_user(username=username,
                                        email=username,
                                        password=password)
        user.save()

        socket_id = '/user/' + str(user.id) + '/'

        additional_user_information = AdditionalUserInformation(user=user, role=Role.USER, socket_id=socket_id)
        additional_user_information.save()

        return True
