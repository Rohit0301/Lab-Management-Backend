from .models import Session
from .utils import FetchUserSession
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


class FetchUserBySessionId(APIView):

    def get(self, request):
        try:
            session = FetchUserSession(request)
            return Response({'session_id': session.session_id, 'role': session.role, 'user_id': session.user_id})
        except:
            raise Exception("Invalid session, please login again")


class SessionLogoutView(APIView):

    def post(self, request):
        try:
            session = FetchUserSession(request)
            old_user_session = Session.objects.get(
                session_id=session.session_id)
            old_user_session.is_deleted = True
            old_user_session.save()
            return Response("Logout Successfully", status=status.HTTP_200_OK)
        except:
            raise Exception("Something went wrong!")
