from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
from django.utils.timezone import now
# from student.models import Student



class TeacherManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError("The Email field must be set")
        user = self.model(email=self.normalize_email(email), name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        user = self.create_user(email=email, name=name, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Teacher(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Add related_name to avoid clashes with the default auth.User model
    groups = models.ManyToManyField(
        Group,
        related_name="teacher_groups",  # Custom related name for Teacher
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="teacher_user_permissions",  # Custom related name for Teacher
        blank=True,
    )

    objects = TeacherManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email


# subject/models.py
class Subject(models.Model):
    subject_code = models.CharField(max_length=20, unique=True)
    subject_name = models.CharField(max_length=100)
    teacher = models.ForeignKey(
        Teacher, 
        on_delete=models.CASCADE,  # Deletes the subject if the associated teacher is deleted
        related_name="subjects",  # Allows reverse lookup (e.g., teacher.subjects.all())
    )
    semester = models.PositiveIntegerField()  # Use PositiveIntegerField to enforce non-negative values
    is_active = models.BooleanField(default=False)
    current_location = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.subject_name} ({self.subject_code}) - Semester {self.semester}"



