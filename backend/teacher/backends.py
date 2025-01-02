from django.contrib.auth.backends import ModelBackend
from teacher.models import Teacher

class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Authenticate user using email as the username
            teacher = Teacher.objects.get(email=username)
            if teacher.check_password(password) and self.user_can_authenticate(teacher):
                return teacher
        except Teacher.DoesNotExist:
            return None
