
from Session import utils as SessionUtils
from Lab import utils as LabUtils
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from .models import UserDetail
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer
from rest_framework import generics, exceptions, status
import sys
sys.path.append("..Session")
sys.path.append("..Lab")


class UserLoginAPIView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):

        email_id = request.data['email_id']
        password = request.data['password']
        if (email_id is None) or (password is None):
            raise exceptions.AuthenticationFailed(
                'username and password required')
        try:
            user = UserDetail.objects.get(
                email_id=email_id)
        except:
            raise exceptions.AuthenticationFailed(
                'Invalid username or password')
        if (user is None or not user.match_password(password)):
            raise exceptions.AuthenticationFailed(
                'Invalid username or password')
        serialized_user = UserLoginSerializer(user).data
        session_id = SessionUtils.CreateOrGetSession(user.id, "user")
        return Response(
            {**serialized_user, 'session_id': session_id},
            status=status.HTTP_200_OK
        )


class UserRegistrationAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer

    def get_queryset(self):
        return


class FetchUserAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = UserDetail.objects.all()


class FetchUserReportsAPIView(APIView):

    def get(self, request):
        session = SessionUtils.FetchUserSession(request)
        user_id = session.user_id
        user = UserDetail.objects.get(id=user_id)
        patient_with_same_email = LabUtils.FetchAllPatients(user.email_id)
        data = []
        for patient in patient_with_same_email:
            bills = LabUtils.PatientBillDetails(patient.id)
            for bill in bills:
                data.append(LabUtils.PatientTestDetailsByBillId(bill['bill']))
        return Response(list(reversed(data)), status=status.HTTP_200_OK)
