from rest_framework import serializers
from .models import Teacher
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class RegisterTeacherSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Teacher
        fields = ['id','email', 'name', 'password']

    def create(self, validated_data):
        return Teacher.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )

class CustomTeacherTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        attrs['username'] = attrs.get('username')  # Map username to email
        return super().validate(attrs)
