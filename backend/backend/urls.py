from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/students/', include('student.urls')),
    path('api/teachers/', include('teacher.urls')),
    
]
