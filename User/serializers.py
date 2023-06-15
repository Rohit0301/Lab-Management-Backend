from rest_framework import serializers
from .models import UserDetail
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserDetail
        fields = ('full_name', 'email_id')


class UserLoginSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    email_id = serializers.EmailField(
        required=True
    )
    password = serializers.CharField(
        write_only=True, required=True)

    class Meta:
        model = UserDetail
        fields = '__all__'


class UserRegistrationSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    email_id = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=UserDetail.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = UserDetail
        fields = ('email_id', 'id', 'password', 'full_name')

    def create(self, validated_data):
        lab = UserDetail.objects.create(
            full_name=validated_data['full_name'],
            email_id=validated_data['email_id'],
        )
        lab.set_password(validated_data['password'])
        lab.save()
        return lab
