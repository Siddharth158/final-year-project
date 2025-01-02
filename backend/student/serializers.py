from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import Student
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from teacher.models import Subject

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'subject_name', 'subject_code', 'semester', 'is_active', 'current_location']

class RegisterStudentSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    subjects = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all(), many=True, required=False)
    enrolled_subjects = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all(), many=True, write_only=True)

    class Meta:
        model = Student
        fields = ['email', 'usn', 'name', 'password', 'is_verified','subjects', 'enrolled_subjects']

    def create(self, validated_data):
        # Extract and remove `subjects` from the validated data
        subjects = validated_data.pop('subjects', [])

        # Create the student object
        student = Student.objects.create_user(
            email=validated_data['email'],
            usn=validated_data['usn'],
            name=validated_data['name'],
            password=validated_data['password']
        )

        # Add subjects to the student
        student.subjects.set(subjects)  # Assign subjects to the student
        return student


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Map `username` to `usn` for authentication
        username = attrs.get('username')  # `username` will carry the `usn` value
        password = attrs.get('password')

        # Authenticate the user
        if username and password:
            user = authenticate(request=self.context.get('request'), usn=username, password=password)
            if not user:
                raise AuthenticationFailed('No active account found with the given credentials')
        else:
            raise AuthenticationFailed('Username and password are required')

        # Generate token pair for authenticated user
        refresh = self.get_token(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return data
    