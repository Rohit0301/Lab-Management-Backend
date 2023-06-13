from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from .models import LabDetail, TestDetail, PatientDetail, BillDetail, PatientTestDetail
from rest_framework.response import Response
from .serializers import LabRegistrationSerializer, LabLoginSerializer, LabTestSerializer, LabPatientSerializer, PatientAssignTestSerializer
from rest_framework import generics, exceptions, status
from django.core import serializers
import json


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

        return Response(
            serialized_user, status=status.HTTP_200_OK)


class LabRegistrationAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LabRegistrationSerializer

    def get_queryset(self):
        return


class TestAPIView(generics.DestroyAPIView, generics.CreateAPIView, generics.UpdateAPIView):
    serializer_class = LabTestSerializer
    queryset = TestDetail.objects.all()


class PatientAPIView(generics.DestroyAPIView, generics.CreateAPIView, generics.UpdateAPIView):
    serializer_class = LabPatientSerializer
    queryset = PatientDetail.objects.all()


def CreateNewBill(total_amount):
    bill = BillDetail.objects.create(total_amount=total_amount)
    bill.save()
    return bill


class PatientAssignTestAPIView(APIView):
    serializer_class = PatientAssignTestSerializer

    def get(self, request, lab_id):
        try:
            test_details = PatientTestDetail.objects.select_related().filter(lab=lab_id)
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

    def post(self, request, lab_id):
        try:
            data = request.data
            bill = CreateNewBill(data['total_amount'])
            patient = PatientDetail.objects.get(id=data['patient_id'])
            lab = LabDetail.objects.get(id=lab_id)

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

    def get(self, request, lab_id):
        tests = list(TestDetail.objects.filter(lab=lab_id))
        serialized_data = json.loads(serializers.serialize("json", tests))
        data = [{**item['fields'], 'id':item['pk']}
                for item in serialized_data]
        return Response(data, status=status.HTTP_200_OK)


class PatientFetchAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LabPatientSerializer

    def get(self, request, lab_id):
        patient_list = PatientDetail.objects.filter(lab=lab_id)
        serialized_data = json.loads(
            serializers.serialize("json", patient_list))
        data = [{**item['fields'], 'id':item['pk']}
                for item in serialized_data]
        return Response(data, status=status.HTTP_200_OK)

# class TestUpdateAPIView(APIView):
#     serializer_class = LabTestSerializer

#     def patch(self, request, test_id):
#         test = TestDetail.objects.get(id=test_id)
#         serializer = LabTestSerializer(
#             test, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, test_id):
#         test = TestDetail.objects.get(id=test_id)
#         if (test):
#             test.delete()
#             return Response({"data": "Test deleted successfully"}, status=status.HTTP_200_OK)
#         else:
#             return Response("Something went wrong", status=status.HTTP_400_BAD_REQUEST)


# class TestCreateAPIView(APIView):
#     serializer_class = LabTestSerializer

#     def post(self, request):
#         test_serializer = LabTestSerializer(data=request.data)
#         if test_serializer.is_valid():
#             test_serializer.save()
#             return Response(test_serializer.data, status=status.HTTP_201_CREATED)
#         return Response(test_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class PatientUpdateAPIView(APIView):
#     serializer_class = LabPatientUpdateSerializer

#     def patch(self, request, patient_id):
#         patient = PatientDetail.objects.get(id=patient_id)
#         serializer = LabPatientUpdateSerializer(
#             patient, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, patient_id):
#         patient = PatientDetail.objects.get(id=patient_id)
#         if (patient):
#             patient.delete()
#             return Response({"data": "Patient deleted successfully"}, status=status.HTTP_200_OK)
#         else:
#             return Response("Something went wrong", status=status.HTTP_400_BAD_REQUEST)
