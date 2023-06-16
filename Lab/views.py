from Session import utils as SessionUtils
from Lab import utils as LabUtils
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from .models import LabDetail, TestDetail, PatientDetail, BillDetail, PatientTestDetail
from rest_framework.response import Response
from .serializers import LabRegistrationSerializer, LabLoginSerializer, LabTestSerializer, LabPatientSerializer, PatientAssignTestSerializer
from rest_framework import generics, exceptions, status
from django.core import serializers
import json
import sys
sys.path.append("..Session")
sys.path.append("..Lab")


class LabLoginAPIView(APIView):
    serializer_class = LabLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        email_id = request.data['email_id']
        password = request.data['password']
        if (email_id is None) or (password is None):
            raise exceptions.AuthenticationFailed(
                'username and password required')
        lab = LabDetail.objects.get(
            email_id=email_id)
        print(lab.match_password(password))
        if (lab is None or not lab.match_password(password)):
            raise exceptions.AuthenticationFailed(
                'Invalid username or password')
        serialized_user = LabLoginSerializer(lab).data
        session_id = SessionUtils.CreateOrGetSession(lab.id, "laboratory")
        return Response(
            {**serialized_user, 'session_id': session_id}, status=status.HTTP_200_OK)


class LabRegistrationAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LabRegistrationSerializer

    def get_queryset(self):
        return


class FetchLabAPIView(generics.RetrieveAPIView):
    serializer_class = LabLoginSerializer
    queryset = LabDetail.objects.all()


class TestAPIView(generics.DestroyAPIView, generics.CreateAPIView, generics.UpdateAPIView):
    serializer_class = LabTestSerializer
    queryset = TestDetail.objects.all()

    def destroy(self, request, pk):
        try:
            session = SessionUtils.FetchUserSession(request)
            old_test = TestDetail.objects.get(id=pk,
                                              lab=session.user_id)
            old_test.is_deleted = True
            old_test.save()
            return Response({'id': old_test.id}, status=status.HTTP_200_OK)
        except:
            raise Exception("Test not found")


class PatientAPIView(generics.DestroyAPIView, generics.CreateAPIView, generics.UpdateAPIView):
    serializer_class = LabPatientSerializer
    queryset = PatientDetail.objects.all()

    def destroy(self, request, pk):
        try:
            session = SessionUtils.FetchUserSession(request)
            old_patient = PatientDetail.objects.get(id=pk,
                                                    lab=session.user_id)
            old_patient.is_deleted = True
            old_patient.save()
            return Response({'id': old_patient.id}, status=status.HTTP_200_OK)
        except:
            raise Exception("Patient not found")


class PatientAssignTestAPIView(APIView):
    serializer_class = PatientAssignTestSerializer

    def get(self, request,):
        try:
            session = SessionUtils.FetchUserSession(request)
            test_details = PatientTestDetail.objects.select_related().filter(lab=session.user_id)
            data = []
            for details in test_details:
                patient = details.patient
                bill = details.bill
                test = details.test
                temp_data = {
                    "id": details.id,
                    "patient_name": f"{patient.first_name} {patient.last_name}",
                    "test_price": test.price,
                    "test_name": test.name,
                    "sample_needed": test.sample_needed,
                    "bill_no": bill.id,
                    "date_time": bill.created_at
                }
                data.append(temp_data)
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response("Something went wrong", status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            session = SessionUtils.FetchUserSession(request)
            data = request.data
            bill = LabUtils.CreateNewBill(data['total_amount'])
            patient = PatientDetail.objects.get(id=data['patient_id'])
            lab = LabDetail.objects.get(id=session.user_id)
            all_tests = []
            for test_id in data['test_ids']:
                test = TestDetail.objects.get(id=test_id)
                all_tests.append(PatientTestDetail(
                    bill=bill, patient=patient, lab=lab, test=test))
            patient_tests = PatientTestDetail.objects.bulk_create(all_tests)
            print(patient_tests)

            return Response("Test assigned to patient", status=status.HTTP_201_CREATED)
        except:
            return Response("Something went wrong", status=status.HTTP_400_BAD_REQUEST)


class TestFetchAPIView(APIView):
    serializer_class = LabTestSerializer
    permission_classes = (AllowAny,)

    def get(self, request):
        session = SessionUtils.FetchUserSession(request)
        tests = list(TestDetail.objects.filter(
            lab=session.user_id, is_deleted=False))
        serialized_data = json.loads(serializers.serialize("json", tests))
        data = [{**item['fields'], 'id':item['pk']}
                for item in serialized_data]
        return Response(data, status=status.HTTP_200_OK)


class PatientFetchAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LabPatientSerializer

    def get(self, request):
        session = SessionUtils.FetchUserSession(request)
        patient_list = PatientDetail.objects.filter(
            lab=session.user_id, is_deleted=False)
        serialized_data = json.loads(
            serializers.serialize("json", patient_list))
        data = [{**item['fields'], 'id':item['pk']}
                for item in serialized_data]
        return Response(data, status=status.HTTP_200_OK)


class FetchPatientByEmailID(APIView):

    def get(self, request):
        try:
            session = SessionUtils.FetchUserSession(request)
            email_id = request.GET.get('email_id')
            data = []
            if email_id:
                patients = PatientDetail.objects.filter(
                    email_id__startswith=email_id, lab=session.user_id, is_deleted=False)
                for patient in patients:
                    temp_data = {
                        "id": patient.id,
                        "patient_name": patient.first_name+' '+patient.last_name,
                        "email_id": patient.email_id
                    }
                    data.append(temp_data)
            return Response(data, status=status.HTTP_200_OK)
        except:
            raise Exception("User not found!",
                            status=status.HTTP_404_NOT_FOUND)


class FetchTestsByName(APIView):

    def get(self, request):
        try:
            session = SessionUtils.FetchUserSession(request)
            test_name = request.GET.get('name')
            data = []
            if test_name:
                tests = TestDetail.objects.filter(
                    name__startswith=test_name, lab=session.user_id, is_deleted=False)
                for test in tests:
                    temp_data = {
                        "id": test.id,
                        "test_name": test.name,
                        "sample_needed": test.sample_needed,
                        "test_type": test.test_type,
                        "price": test.price
                    }
                    data.append(temp_data)
            return Response(data, status=status.HTTP_200_OK)
        except:
            raise Exception("Test not found!",
                            )


class PatientReports(APIView):

    def get(self, request):
        session = SessionUtils.FetchUserSession(request)
        lab_id = session.user_id
        patients = PatientDetail.objects.filter(lab=lab_id)
        data = []
        for patient in patients:
            bills = LabUtils.PatientBillDetails(patient.id)
            bill_ids = []
            report_data = []
            for bill in bills:
                bill_ids.append(bill['bill'])
                temp_bills = LabUtils.PatientRepostDetails(bill['bill'])
                report_data.extend(temp_bills)
            if len(report_data) == 0:
                continue
            temp_data = {
                'id': patient.id,
                'patient_name': patient.first_name+' '+patient.last_name,
                'patient_email': patient.email_id,
                'reports': report_data,
                'bill_ids': bill_ids
            }
            data.append(temp_data)

        return Response(data)
