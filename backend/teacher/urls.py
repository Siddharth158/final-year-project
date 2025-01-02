from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterTeacherView, CustomTeacherTokenObtainPairView, TeacherLogoutView, CreateSubjectView, SubjectListView, ToggleIsActiveView, GetTeacherDataView

urlpatterns = [
    path('register/', RegisterTeacherView.as_view(), name='teacher-register'),
    path('login/', CustomTeacherTokenObtainPairView.as_view(), name='teacher-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='teacher-token-refresh'),
    path('logout/', TeacherLogoutView.as_view(), name='teacher-logout'),
    path('subjects/create/', CreateSubjectView.as_view(), name='create_subject'),
    path('subjects/<int:teacher_id>/', SubjectListView.as_view(), name='subject_list'),
    path('subjects/toggle/<int:subject_id>/', ToggleIsActiveView.as_view(), name='toggle_is_active'),
    path('get-teacher-data/', GetTeacherDataView.as_view(), name='get-teacher-data'),
]
