from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
from teacher.models import Subject  # Import Subject model
from django.utils.timezone import now

class StudentManager(BaseUserManager):
    def create_user(self, usn, name, email, password=None):
        if not usn:
            raise ValueError("The USN field must be set")
        if not email:
            raise ValueError("The Email field must be set")
        user = self.model(usn=usn, name=name, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, usn, name, email, password=None):
        user = self.create_user(usn=usn, name=name, email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Student(AbstractBaseUser, PermissionsMixin):
    usn = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    # New field for enrolled subjects
    subjects = models.ManyToManyField(
        Subject,  # Reference the Subject model
        related_name="enrolled_students",  # Reverse relation to list students in a subject
        blank=True
    )

    # Avoid clashes by setting unique related names
    groups = models.ManyToManyField(
        Group,
        related_name="student_groups",  # Custom related name for this model
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="student_permissions",  # Custom related name for this model
        blank=True,
    )

    objects = StudentManager()

    USERNAME_FIELD = 'usn'
    REQUIRED_FIELDS = ['name', 'email']

    def __str__(self):
        return self.usn


class AttendanceSheet(models.Model):
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,  # Deletes attendance records if the subject is deleted
        related_name="attendance_records",  # Reverse lookup for subject attendance
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,  # Deletes attendance records if the student is deleted
        related_name="attendance_records",  # Reverse lookup for student attendance
    )
    date_time = models.DateTimeField(default=now)  # Automatically captures the date and time when attendance is marked

    class Meta:
        unique_together = ('subject', 'student', 'date_time')  # Ensures no duplicate records for the same student, subject, and date_time
        verbose_name = "Attendance Record"
        verbose_name_plural = "Attendance Records"

    def __str__(self):
        return f"Attendance for {self.student.usn} in {self.subject.subject_code} on {self.date_time.strftime('%Y-%m-%d %H:%M:%S')}"
