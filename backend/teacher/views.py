from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .serializers import RegisterTeacherSerializer, CustomTeacherTokenObtainPairSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from .models import Subject, Teacher
import json
import jwt

# Register View
class RegisterTeacherView(APIView):
    authentication_classes = []  # Disable authentication for this view
    permission_classes = []  # Disable permission checks for this view

    def post(self, request):
        serializer = RegisterTeacherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Registration successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login View
class CustomTeacherTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTeacherTokenObtainPairSerializer

# Logout View
class TeacherLogoutView(APIView):
    # Disable authentication and permission checks
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        try:
            # Extract the refresh token from the request body
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({'detail': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

            # Validate the refresh token
            token = RefreshToken(refresh_token)

            # If token is valid, the logout is considered successful
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)

        except TokenError:
            return Response({'detail': 'Invalid or expired refresh token'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'detail': f'An unexpected error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetTeacherDataView(APIView):
    authentication_classes = []  # Disable authentication
    permission_classes = []  # Disable permissions

    def get(self, request):
        try:
            # print("hello") 
            token = request.headers.get('Authorization')
            if not token:
                return Response({"detail": "Authorization token is missing"}, status=status.HTTP_401_UNAUTHORIZED)

            # Decode the JWT token
            final_token = token.split(' ')[1]
            decoded_payload = jwt.decode(final_token, options={"verify_signature": False})
            # print(decoded_payload)

            # Fetch user_id from the token payload
            user_id = decoded_payload.get('user_id')
            if not user_id:
                return Response({"detail": "User ID not found in token"}, status=status.HTTP_400_BAD_REQUEST)
            # print(user_id)
            
            # Fetch the student using the primary key (id)
            teacher = Teacher.objects.get(id=user_id)
            # print(student)
            
            # Serialize the student data
            serializer = RegisterTeacherSerializer(teacher)
            # print(serializer.data)

            # Return the serialized data
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Teacher.DoesNotExist:
            return Response({"detail": "Student not found with the provided user_id"}, status=status.HTTP_404_NOT_FOUND)
        except jwt.DecodeError:
            return Response({"detail": "Invalid JWT token"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class CreateSubjectView(View):

    def post(self, request):
        try:
            # Parse JSON data from the request
            data = json.loads(request.body)
            subject_code = data.get('subject_code')
            subject_name = data.get('subject_name')
            semester = data.get('semester')
            teacher_id = data.get('teacher_id')

            # Validate required fields
            if not all([subject_code, subject_name, semester, teacher_id]):
                return JsonResponse({"error": "All fields are required."}, status=400)

            # Ensure the teacher exists
            try:
                teacher = Teacher.objects.get(pk=teacher_id)
            except Teacher.DoesNotExist:
                return JsonResponse({"error": "Teacher not found."}, status=404)

            # Create the new subject
            subject = Subject.objects.create(
                subject_code=subject_code,
                subject_name=subject_name,
                semester=semester,
                teacher=teacher,
                is_active=False  # Default to active
            )

            # Respond with the created subject's details
            return JsonResponse({
                "message": "Subject created successfully.",
                "subject": {
                    "id": subject.id,
                    "subject_code": subject.subject_code,
                    "subject_name": subject.subject_name,
                    "semester": subject.semester,
                    "teacher": teacher.name,
                    "is_active": subject.is_active
                }
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON input."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


class SubjectListView(View):
    def get(self, request, teacher_id):
        try:
            # Fetch subjects for the given teacher
            print(teacher_id)
            subjects = Subject.objects.filter(teacher_id=teacher_id)
            subject_list = [
                {
                    "id": subject.id,
                    "subject_code": subject.subject_code,
                    "subject_name": subject.subject_name,
                    "semester": subject.semester,
                    "is_active": subject.is_active,
                }
                for subject in subjects
            ]
            return JsonResponse({"subjects": subject_list}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')       
class ToggleIsActiveView(View):
    def post(self, request, subject_id):
        try:
            # Retrieve the subject by ID
            subject = Subject.objects.get(id=subject_id)

            # Parse the incoming request body
            data = json.loads(request.body)
            current_location = data.get("current_location", "")  # Get current location from request

            # Check current status and toggle
            if not subject.is_active:
                # If is_active is being set to True, update current_location
                subject.current_location = current_location
            else:
                # If is_active is being set to False, clear current_location
                subject.current_location = ""

            # Toggle the is_active field
            subject.is_active = not subject.is_active
            subject.save()

            return JsonResponse({
                "message": "Subject status updated successfully.",
                "subject": {
                    "id": subject.id,
                    "subject_code": subject.subject_code,
                    "subject_name": subject.subject_name,
                    "is_active": subject.is_active,
                    "current_location": subject.current_location,  # Include the updated location
                }
            }, status=200)
        except Subject.DoesNotExist:
            return JsonResponse({"error": "Subject not found."}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
