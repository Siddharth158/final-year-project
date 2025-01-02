from django.contrib import admin
from .models import Student, AttendanceSheet

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'usn', 'is_active', 'is_verified')
    
@admin.register(AttendanceSheet)
class AttendanceSheetAdmin(admin.ModelAdmin):
    list_display = ('subject', 'date_time', 'student')
