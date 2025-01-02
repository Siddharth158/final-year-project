from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Teacher
from .models import Subject

class TeacherAdmin(UserAdmin):
    # Specify the fields to display in the admin panel
    list_display = ('email', 'name', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'name')
    ordering = ('email',)

    # Define the fieldsets for viewing/editing a teacher in the admin panel
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    # Define the fields to use when adding a new teacher in the admin panel
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )

# Register the Teacher model
admin.site.register(Teacher, TeacherAdmin)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('subject_code', 'subject_name', 'teacher', 'semester', 'is_active')
    list_filter = ('semester', 'is_active')
    search_fields = ('subject_code', 'subject_name', 'teacher__name')
    ordering = ('semester', 'subject_name')