from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterStudentView, LogoutView, CustomTokenObtainPairView, GetStudentDataView, GetSubjectsByIdsView
from .views import create_dataset, enroll_student_in_subject, search_subjects, mark_attendance

urlpatterns = [
    path('register/', RegisterStudentView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('get-student-data/', GetStudentDataView.as_view(), name='get-student-data'),
    path("create-dataset/", create_dataset, name="create-dataset"),
    path("subjects/search", search_subjects, name="search_subjects"),
    path("enroll/", enroll_student_in_subject, name="enroll_student"),
    path('get-subjects-by-ids/', GetSubjectsByIdsView.as_view(), name='get_subjects_by_ids'),
    path('mark_attendance/', mark_attendance, name='mark_attendance'),
]
