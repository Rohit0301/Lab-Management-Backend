from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from .models import Session


class SessionAuthentication(BaseAuthentication):

    def authenticate(self, request):
        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            return None
        try:
            session_id = authorization_header.split(' ')[1]
            session = Session.objects.get(session_id=session_id)
        except:
            raise exceptions.AuthenticationFailed('User not found.')

        return (session, None)
