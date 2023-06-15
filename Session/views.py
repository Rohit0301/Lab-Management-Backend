from .models import Session
from .utils import FetchUserSession
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


class FetchUserBySessionId(APIView):

    def get(self, request):
        try:
            auth_headers = request.headers.get('Authorization')
            if (not auth_headers):
                raise Exception("Invalid session!")
            session_id = auth_headers.split(' ')[1]
            session = FetchUserSession(session_id)
            return Response({'session_id': session_id, 'role': session.role, 'user_id': session.user_id})
        except:
            raise Exception("Invalid session, please login again")


class SessionLogoutView(APIView):

    def post(self, request):
        try:
            auth_headers = request.headers.get('Authorization')
            if (not auth_headers):
                raise Exception("Invalid session!")
            session_id = auth_headers.split(' ')[1]
            session = Session.objects.get(session_id=session_id)
            session.is_deleted = True
            session.save()
            return Response("Logout Successfully", status=status.HTTP_200_OK)
        except:
            raise Exception("Something went wrong!")
