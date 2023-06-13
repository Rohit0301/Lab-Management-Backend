from rest_framework import serializers
from .models import LabDetail, TestDetail, PatientDetail, PatientTestDetail
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator


class LabLoginSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = LabDetail
        exclude = ('password',)


class PatientAssignTestSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = PatientTestDetail
        fields = '__all__'


class LabTestSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = TestDetail
        fields = '__all__'


class LabRegistrationSerializer(serializers.ModelSerializer):
    email_id = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=LabDetail.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = LabDetail
        fields = ('email_id', 'password',
                  'phone_no', 'name', 'address', 'id')
        extra_kwargs = {
            'address': {'required': True},
            'name': {'required': True},
            'phone_no': {'required': True}
        }

    def create(self, validated_data):
        lab = LabDetail.objects.create(
            name=validated_data['name'],
            email_id=validated_data['email_id'],
            address=validated_data['address'],
            phone_no=validated_data['phone_no']
        )
        lab.set_password(validated_data['password'])
        lab.save()
        return lab


class LabPatientSerializer(serializers.ModelSerializer):
    email_id = serializers.EmailField(
        required=True,
    )
    age = serializers.IntegerField(
        required=True,
        min_value=0,
        max_value=150
    )
    gender = serializers.ChoiceField(
        required=True,
        choices=['Male', 'Female']
    )

    class Meta:
        model = PatientDetail
        fields = '__all__'
        extra_kwargs = {
            'address': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'phone_no': {'required': True}
        }

    def validate(self, data):
        email_id = data['email_id']
        labs = LabDetail.objects.filter(email_id=email_id)
        if labs:
            raise serializers.ValidationError(
                "Patient can't used registered lab email id")
        return data
