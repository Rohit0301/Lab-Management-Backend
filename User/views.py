from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from .models import UserDetail
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer, UserLoginSerializer
from rest_framework import generics, exceptions, status


class UserLoginAPIView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        email_id = request.data['email_id']
        password = request.data['password']
        if (email_id is None) or (password is None):
            raise exceptions.AuthenticationFailed(
                'username and password required')
        user = UserDetail.objects.get(
            email_id=email_id)
        if (user is None or not user.match_password(password)):
            raise exceptions.AuthenticationFailed(
                'Invalid username or password')
        serialized_user = UserLoginSerializer(user).data
        return Response(
            serialized_user, status=status.HTTP_200_OK)


class UserRegistrationAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer

    def get_queryset(self):
        return
