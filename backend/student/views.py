from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .serializers import CustomTokenObtainPairSerializer
from .serializers import RegisterStudentSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Student, AttendanceSheet
from rest_framework.decorators import api_view
from .authentication import DebugJWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from datetime import timedelta
import jwt
import os
import base64
from pathlib import Path
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import numpy as np
import cv2
import json
from face_recognition.face_recognition_cli import image_files_in_folder
from teacher.models import Subject
from rest_framework.decorators import api_view, permission_classes
from .serializers import SubjectSerializer
from django.shortcuts import get_object_or_404
from PIL import Image
import io
from sklearn.svm import SVC
from albumentations import (
    HorizontalFlip,
    RandomBrightnessContrast,
    GaussNoise,
    Rotate,
    RandomGamma,
    Blur,
    Compose
)

# Register View
class RegisterStudentView(APIView):
    authentication_classes = []  # Disable authentication for this view
    permission_classes = []  # Disable permission checks for this view

    def post(self, request):
        print(request.data)
        serializer = RegisterStudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Registration successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Login View
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# Logout View
class LogoutView(APIView):
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
        

        
class GetStudentDataView(APIView):
    authentication_classes = []  # Disable authentication
    permission_classes = []  # Disable permissions

    def get(self, request):
        try:
            print("hello") 
            token = request.headers.get('Authorization')
            if not token:
                return Response({"detail": "Authorization token is missing"}, status=status.HTTP_401_UNAUTHORIZED)

            # Decode the JWT token
            final_token = token.split(' ')[1]
            decoded_payload = jwt.decode(final_token, options={"verify_signature": False})
            print(decoded_payload)

            # Fetch user_id from the token payload
            user_id = decoded_payload.get('user_id')
            if not user_id:
                return Response({"detail": "User ID not found in token"}, status=status.HTTP_400_BAD_REQUEST)
            print(user_id)
            
            # Fetch the student using the primary key (id)
            student = Student.objects.get(id=user_id)
            print(student)
            
            # Serialize the student data
            serializer = RegisterStudentSerializer(student)
            print(serializer.data)

            # Return the serialized data
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Student.DoesNotExist:
            return Response({"detail": "Student not found with the provided user_id"}, status=status.HTTP_404_NOT_FOUND)
        except jwt.DecodeError:
            return Response({"detail": "Invalid JWT token"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# def create_dataset(request):
#     if request.method == "POST":
#         try:
#             # Extract student data from the request body
#             base_samples=10
#             target_samples=300
#             student_id = request.POST.get("student_id")
#             student_name = request.POST.get("student_name")

#             if not student_id or not student_name:
#                 return JsonResponse({"status": "error", "message": "Student ID and name are required."}, status=400)

#             # Fetch the student from the database
#             student = get_object_or_404(Student, usn=student_id)

#             # Create a directory for the student using their name
#             base_dir = Path("face_recognition_data/training_dataset")
#             user_dir = base_dir / student_name
#             user_dir.mkdir(parents=True, exist_ok=True)

#             # Decode and save base images
#             data = request.POST.get("images")  # Expecting a list of images as base64 strings
#             if not data:
#                 return JsonResponse({"status": "error", "message": "No images provided."}, status=400)

#             images = data.split(",")  # Assuming the images are comma-separated
#             if len(images) != base_samples:
#                 return JsonResponse({
#                     "status": "error",
#                     "message": f"Expected {base_samples} images but received {len(images)}."
#                 }, status=400)

#             total_images = 0
#             for idx, image_data in enumerate(images):
#                 image_data = base64.b64decode(image_data)  # Decode the base64 image data
#                 np_arr = np.frombuffer(image_data, np.uint8)  # Convert bytes to numpy array
#                 img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)  # Decode into an image

#                 # Save the original image
#                 total_images += 1
#                 file_path = user_dir / f"{total_images}.jpg"
#                 cv2.imwrite(str(file_path), img)

#             # Augmentation pipeline
#             augmentor = Compose([
#                 HorizontalFlip(p=0.5),
#                 RandomBrightnessContrast(p=0.7),
#                 GaussNoise(p=0.3),
#                 Rotate(limit=15, p=0.5),
#                 RandomGamma(p=0.3),
#                 Blur(blur_limit=3, p=0.3),
#             ])

#             # Generate augmented images
#             augmentations_per_image = (target_samples - base_samples) // base_samples
#             for idx, image_data in enumerate(images):
#                 image_data = base64.b64decode(image_data)
#                 np_arr = np.frombuffer(image_data, np.uint8)
#                 img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

#                 for _ in range(augmentations_per_image):
#                     augmented = augmentor(image=img)["image"]
#                     total_images += 1
#                     aug_path = user_dir / f"{total_images}.jpg"
#                     cv2.imwrite(str(aug_path), augmented)

#             # Update the student's is_verified field
#             student.is_verified = True
#             student.save()

#             return JsonResponse({
#                 "status": "success",
#                 "message": f"Dataset created with {total_images} images. Student verified."
#             })

#         except Exception as e:
#             return JsonResponse({"status": "error", "message": str(e)}, status=500)

#     return JsonResponse({"status": "error", "message": "Invalid request method."}, status=400)

@csrf_exempt
def create_dataset(request):
    if request.method == "POST":
        try:
            # Extract student data from the request body
            base_samples = 10
            target_samples = 300
            student_id = request.POST.get("student_id")
            student_name = request.POST.get("student_name")

            if not student_id or not student_name:
                return JsonResponse({"status": "error", "message": "Student ID and name are required."}, status=400)

            # Fetch the student from the database
            student = get_object_or_404(Student, usn=student_id)

            # Create a directory for the student using their name
            base_dir = Path("face_recognition_data/training_dataset")
            user_dir = base_dir / student_id
            user_dir.mkdir(parents=True, exist_ok=True)

            # Initialize session tracking
            sample_num = request.session.get('sample_num', 0)
            total_images = request.session.get('total_images', 0)

            if sample_num >= base_samples:
                return JsonResponse({
                    "status": "error",
                    "message": "Base sample limit reached",
                    "completed": True
                })

            # Decode and save base images
            data = request.POST.get("images")  # Expecting a list of images as base64 strings
            if not data:
                return JsonResponse({"status": "error", "message": "No images provided."}, status=400)

            images = data.split(",")  # Assuming the images are comma-separated
            if len(images) != base_samples:
                return JsonResponse({
                    "status": "error",
                    "message": f"Expected {base_samples} images but received {len(images)}."
                }, status=400)

            predictor_path = Path('face_recognition_data/shape_predictor_68_face_landmarks.dat')
            if not predictor_path.exists():
                raise FileNotFoundError(f"Shape predictor file not found at {predictor_path}")

            detector = dlib.get_frontal_face_detector()

            # Process each image
            processed_faces = 0
            for idx, image_data in enumerate(images):
                try:
                    image_data = base64.b64decode(image_data)  # Decode the base64 image data
                    np_arr = np.frombuffer(image_data, np.uint8)  # Convert bytes to numpy array
                    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)  # Decode into an image

                    if img is None:
                        print(f"Failed to decode image {idx}")
                        continue

                    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    faces = detector(gray_frame, 0)

                    if not faces:
                        print(f"No face detected in image {idx}")
                        continue

                    for face in faces:
                        x, y, w, h = face.left(), face.top(), face.width(), face.height()
                        face_region = img[y:y + h, x:x + w]
                        if face_region.size == 0:
                            print(f"Invalid face region in image {idx}")
                            continue

                        face_aligned = cv2.resize(face_region, (256, 256))

                        # Save original image with sequential numbering
                        total_images += 1
                        file_path = user_dir / f"{total_images}.jpg"
                        cv2.imwrite(str(file_path), face_aligned)
                        processed_faces += 1

                        # Augmentation pipeline
                        augmentor = Compose([
                            HorizontalFlip(p=0.5),
                            RandomBrightnessContrast(p=0.7),
                            GaussNoise(p=0.3),
                            Rotate(limit=15, p=0.5),
                            RandomGamma(p=0.3),
                            Blur(blur_limit=3, p=0.3),
                        ])

                        augmentations_per_image = (target_samples - base_samples) // base_samples

                        for _ in range(augmentations_per_image):
                            augmented = augmentor(image=face_aligned)["image"]
                            total_images += 1
                            aug_path = user_dir / f"{total_images}.jpg"
                            cv2.imwrite(str(aug_path), augmented)

                    sample_num += 1
                    request.session['sample_num'] = sample_num
                    request.session['total_images'] = total_images

                except Exception as e:
                    print(f"[WARNING] Face processing error in image {idx}: {str(e)}")
                    continue

            if processed_faces == 0:
                return JsonResponse({
                    "status": "error",
                    "message": "No valid faces were detected in any of the provided images."
                }, status=400)

            # Update the student's is_verified field
            student.is_verified = True
            student.save()
            

            print("Starting training process...")

            # # Training process begins
            # training_dir = 'face_recognition_data/training_dataset'

            # # Load processed images list
            # processed_images_path = 'face_recognition_data/processed_images.pkl'
            # try:
            #     if os.path.exists(processed_images_path):
            #         with open(processed_images_path, 'rb') as f:
            #             processed_images = pickle.load(f)
            #     else:
            #         processed_images = set()
            # except Exception as e:
            #     print(f"Error loading processed images list: {str(e)}")
            #     processed_images = set()

            # # Load existing model and data
            # try:
            #     with open("face_recognition_data/svc.sav", 'rb') as f:
            #         existing_model = pickle.load(f)
            #     existing_classes = np.load('face_recognition_data/classes.npy', allow_pickle=True)
            #     X_existing = np.load('face_recognition_data/X_data.npy', allow_pickle=True)
            #     y_existing = np.load('face_recognition_data/y_data.npy', allow_pickle=True)
            #     print("Loaded existing model data:")
            #     print(f"Existing classes: {existing_classes}")
            #     print(f"Number of existing samples: {len(X_existing)}")
            #     has_existing_data = True
            # except Exception as e:
            #     print(f"No existing model found or error loading model: {str(e)}")
            #     has_existing_data = False
            #     X_existing = []
            #     y_existing = []
            #     existing_model = None
            #     existing_classes = []

            # X_new = []
            # y_new = []
            # new_images_processed = False
            # new_classes_added = set()

            # # Get list of folders in training directory
            # people_folders = [f for f in os.listdir(training_dir) 
            #                  if os.path.isdir(os.path.join(training_dir, f))]
            
            # print(f"Number of people folders: {len(people_folders)}")
            # print(f"People folders: {people_folders}")

            # # First, identify new people/classes
            # new_people = [person for person in people_folders 
            #              if person not in existing_classes]
            
            # print(f"Number of new people: {len(new_people)}")
            # print(f"New people: {new_people}")

            # if not new_people:
            #     print('No new people to train. All existing folders are already trained.')
            #     return JsonResponse({
            #         "status": "success",
            #         "message": "Dataset created and no new people to train."
            #     })

            # # Process only new people's folders
            # for person_name in new_people:
            #     curr_directory = os.path.join(training_dir, person_name)
            #     print(f"Processing new person: {person_name}")
            #     new_classes_added.add(person_name)

            #     person_images_processed = 0
            #     for imagefile in image_files_in_folder(curr_directory):
            #         abs_path = os.path.abspath(imagefile)
            #         if abs_path in processed_images:
            #             continue

            #         print(f"Processing new image: {imagefile}")
            #         image = cv2.imread(imagefile)

            #         if image is None:
            #             print(f"Failed to load image: {imagefile}")
            #             continue

            #         try:
            #             face_encodings = face_recognition.face_encodings(image)
            #             if not face_encodings:
            #                 print(f"No face detected in {imagefile}")
            #                 continue
                            
            #             face_encoding = face_encodings[0].tolist()
            #             X_new.append(face_encoding)
            #             y_new.append(person_name)
            #             processed_images.add(abs_path)
            #             new_images_processed = True
            #             person_images_processed += 1
            #         except Exception as e:
            #             print(f"Error processing {imagefile}: {str(e)}")
            #             continue

            #     if person_images_processed == 0:
            #         print(f"Warning: No valid face encodings processed for {person_name}")

            # print(f"Number of successful encodings: {len(X_new)}")

            # # If no new data, return early
            # if not new_images_processed:
            #     print('No new images were successfully processed')
            #     return JsonResponse({
            #         "status": "success",
            #         "message": "Dataset created but no new images were processed."
            #     })

            # # Save updated list of processed images
            # with open(processed_images_path, 'wb') as f:
            #     pickle.dump(processed_images, f)

            # # Check if we have enough classes for training
            # if has_existing_data:
            #     all_classes = set(existing_classes).union(new_classes_added)
            # else:
            #     all_classes = new_classes_added

            # if len(all_classes) < 2:
            #     return JsonResponse({
            #         "status": "error",
            #         "message": "Need at least two different people to train the model. Please add more people's data."
            #     })

            # # Combine new data with existing data and train
            # print("Adding new person data to model...")
            # if has_existing_data:
            #     X = np.vstack((X_existing, np.array(X_new)))
            #     y = np.concatenate((y_existing, np.array(y_new)))
            # else:
            #     X = np.array(X_new)
            #     y = np.array(y_new)

            # # Verify we have enough samples for each class
            # unique_classes, class_counts = np.unique(y, return_counts=True)
            # min_samples_per_class = 1  # Adjust this threshold as needed
            
            # classes_with_few_samples = [
            #     (cls, count) for cls, count in zip(unique_classes, class_counts)
            #     if count < min_samples_per_class
            # ]
            
            # if classes_with_few_samples:
            #     return JsonResponse({
            #         "status": "error",
            #         "message": f"Some classes have too few samples: {classes_with_few_samples}. Need at least {min_samples_per_class} samples per person."
            #     })

            # # Train new model with all data
            # print("Training updated model...")
            # svc = SVC(kernel='linear', probability=True)
            # svc.fit(X, y)

            # # Save updated model and data
            # print("Saving updated model and data...")
            # np.save('face_recognition_data/X_data.npy', X)
            # np.save('face_recognition_data/y_data.npy', y)
            # np.save('face_recognition_data/classes.npy', np.unique(y))

            # with open("face_recognition_data/svc.sav", 'wb') as f:
            #     pickle.dump(svc, f)

            # # Calculate accuracy metrics
            # accuracy = svc.score(X, y)

            # print(f"Model accuracy: {accuracy:.2f}")
            # print(f"Added {len(new_people)} new people: {', '.join(new_people)}")
            # print(f"Processed {len(X_new)} new images")
            # print(f"Total samples after update: {len(X)}")
            # print(f"Total classes after update: {len(np.unique(y))}")

            # return JsonResponse({
            #     "status": "success",
            #     "message": f"Dataset created and training completed. Added {len(new_people)} new people ({', '.join(new_people)}) with {len(X_new)} images. Current accuracy: {accuracy:.2f}",
            #     "accuracy": accuracy
            # })
            return JsonResponse({
                "status": "success",
                "message": "Dataset created successfully."
            })

        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return JsonResponse({
                "status": "error", 
                "message": f"An unexpected error occurred: {str(e)}"
            }, status=500)

    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=400)


    

def search_subjects(request):
    code = request.GET.get("code", "")
    
    if not code:
        return JsonResponse({"error": "Subject code is required."}, status=400)

    subjects = Subject.objects.filter(subject_code__icontains=code)
    results = [
        {
            "id": subject.id,
            "subject_code": subject.subject_code,
            "subject_name": subject.subject_name,
            "semester": subject.semester,
        }
        for subject in subjects
    ]

    return JsonResponse(results, safe=False)

# Enroll student in a subject
@csrf_exempt
def enroll_student_in_subject(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            subject_id = data.get('subject_id')
            student_id = data.get('student_id')  # Pass student_id explicitly from the request body
            if not subject_id or not student_id:
                return JsonResponse({"error": "Subject ID and Student ID are required."}, status=400)

            # Fetch the subject and student
            subject = Subject.objects.get(id=subject_id)
            student = Student.objects.get(usn=student_id)
            # Check if already enrolled
            if subject in student.subjects.all():
                return JsonResponse({"message": "Student is already enrolled in this subject."}, status=400)

            # Enroll the student in the subject
            student.subjects.add(subject)

            return JsonResponse({
                "message": "Student enrolled successfully.",
                "subject": {
                    "id": subject.id,
                    "subject_code": subject.subject_code,
                    "subject_name": subject.subject_name,
                    "semester": subject.semester,
                    "is_active": subject.is_active,
                }
            }, status=200)

        except Subject.DoesNotExist:
            return JsonResponse({"error": "Subject not found."}, status=404)
        except Student.DoesNotExist:
            return JsonResponse({"error": "Student not found."}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON input."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid HTTP method. Only POST is allowed."}, status=405)
    
    
    
class GetSubjectsByIdsView(APIView):
    authentication_classes = []  # Disable authentication
    permission_classes = []
    def post(self, request):
        try:
            # Get the list of subject IDs from the request body
            subject_ids = request.data.get('subject_ids', [])
            if not subject_ids:
                return Response({"detail": "Subject IDs are required"}, status=status.HTTP_400_BAD_REQUEST)

            # Fetch subjects matching the IDs
            subjects = Subject.objects.filter(id__in=subject_ids)
            if not subjects.exists():
                return Response({"detail": "No subjects found for the provided IDs"}, status=status.HTTP_404_NOT_FOUND)

            # Serialize the subjects
            serializer = SubjectSerializer(subjects, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"detail": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


from django.http import JsonResponse
import json
import base64
import cv2
import numpy as np
import dlib
from imutils import face_utils
from face_recognition import face_locations, face_encodings
from sklearn.preprocessing import LabelEncoder
# from .utils import predict, update_attendance_in_db_in
import datetime
import time
import pickle
import face_recognition
from django.utils.timezone import now



def predict(face_aligned, svc, threshold: float = 0.7) -> tuple:
    if face_aligned is None:
        return ([-1], [0])
        
    try:
        face_locations = face_recognition.face_locations(face_aligned, model="hog")
        if not face_locations:
            return ([-1], [0])
            
        face_encodings = face_recognition.face_encodings(face_aligned, face_locations, model="small")
        if not face_encodings:
            return ([-1], [0])
            
        probabilities = svc.predict_proba(face_encodings)
        max_prob_idx = np.argmax(probabilities[0])
        max_prob = probabilities[0][max_prob_idx]
        
        return ([max_prob_idx], [max_prob]) if max_prob > threshold else ([-1], [max_prob])
        
    except Exception as e:
        print(f"[WARNING] Prediction error: {str(e)}")
        return ([-1], [0])
    
    
def update_attendance_in_db(student_id, subject_code):
    try:
        # Fetch the student and subject objects
        student = Student.objects.get(usn=student_id)
        subject = Subject.objects.get(subject_code=subject_code)
        print(student)
        print(subject)
        

        # Check if attendance record already exists for this student, subject, and date (to avoid duplicates)
        current_time = now()
        time_window_start = current_time - timedelta(minutes=30)

        # Check if an attendance record already exists for this student, subject, and within the time window
        attendance_exists = AttendanceSheet.objects.filter(
            subject=subject,
            student=student,
            date_time__gte=time_window_start,  # Greater than or equal to the start of the time window
            date_time__lte=current_time       # Less than or equal to the current time
        ).exists()

        if attendance_exists:
            print(f"Attendance already marked for {student.usn} in {subject.subject_code}.")
            return False  # Return false if attendance is already marked

        # Create a new attendance record
        AttendanceSheet.objects.create(subject=subject, student=student, date_time=current_time)
        print(f"Attendance marked successfully for {student.usn} in {subject.subject_code}.")
        return True  # Return true if attendance is successfully marked

    except Student.DoesNotExist:
        print(f"Student with ID {student_id} does not exist.")
        raise Exception(f"Student with ID {student_id} does not exist.")
    except Subject.DoesNotExist:
        print(f"Subject with code {subject_code} does not exist.")
        raise Exception(f"Subject with code {subject_code} does not exist.")
    except Exception as e:
        print(f"Error updating attendance: {str(e)}")
        raise Exception(f"Error updating attendance: {str(e)}")
    
@csrf_exempt
def mark_attendance(request):
    if request.method == "POST":
        try:
            # Parse the request data
            data = json.loads(request.body.decode('utf-8'))
            subject_code = data.get("subject_code")
            student_id = data.get("student_id")
            image_data = data.get("image")
            student_name=data.get("student_name")

            if not (subject_code and student_id and image_data):
                return JsonResponse({
                    "status": "error",
                    "message": "Missing required fields: subject_code, student_id, or image."
                }, status=400)

            # Decode the base64 image
            image_data = image_data.split(",")[1]  # Strip base64 header
            image_bytes = base64.b64decode(image_data)
            np_arr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            # Load face detection and recognition models
            detector = dlib.get_frontal_face_detector()
            predictor = dlib.shape_predictor('face_recognition_data/shape_predictor_68_face_landmarks.dat')
            svc_save_path = "face_recognition_data/svc.sav"

            with open(svc_save_path, 'rb') as f:
                svc = pickle.load(f)

            encoder = LabelEncoder()
            encoder.classes_ = np.load('face_recognition_data/classes.npy')

            # Initialize attendance tracking
            faces_encodings = np.zeros((1, 128))
            no_of_faces = len(svc.predict_proba(faces_encodings)[0])
            count = {encoder.inverse_transform([i])[0]: 0 for i in range(no_of_faces)}
            present = {encoder.inverse_transform([i])[0]: False for i in range(no_of_faces)}
            log_time = {}
            start = {}

            # Detect faces
            gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector(gray_frame, 0)

            for face in faces:
                try:
                    x, y, w, h = face_utils.rect_to_bb(face)

                    # Direct face extraction and resizing
                    face_region = img[max(y, 0):min(y+h, img.shape[0]), 
                                      max(x, 0):min(x+w, img.shape[1])]
                    if face_region.size == 0:
                        continue

                    face_aligned = cv2.resize(face_region, (96, 96))

                    pred, prob = predict(face_aligned, svc)

                    if pred != [-1]:
                        person_name = encoder.inverse_transform(np.ravel([pred]))[0]
                        pred = person_name

                        if count[pred] == 0:
                            start[pred] = time.time()
                            count[pred] = count.get(pred, 0) + 1

                        if count[pred] == 4 and (time.time()-start[pred]) > 1.2:
                            count[pred] = 0
                        else:
                            present[pred] = True
                            log_time[pred] = datetime.datetime.now()
                            count[pred] = count.get(pred, 0) + 1
                            print(pred, present[pred], count[pred])
                    else:
                        print("Unknown face detected")

                except Exception as e:
                    print(f"[WARNING] Face processing error: {str(e)}")
                    continue

            # Check if student is recognized
            print(present)
            # if not present.get(student_id, False):
            if not present.get(student_id, False):
                return JsonResponse({
                    "status": "error",
                    "message": "Student not present."
                }, status=404)

            # Update attendance in database
            update_attendance_in_db(student_id, subject_code)

            return JsonResponse({
                "status": "success",
                "message": "Attendance marked successfully.",
                "student_id": student_id,
                "subject_code": subject_code,
                "timestamp": datetime.datetime.now().isoformat()
            })

        except Exception as e:
            print(f"[ERROR] {str(e)}")
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=500)

    return JsonResponse({
        "status": "error",
        "message": "Invalid request method."
    }, status=400)
