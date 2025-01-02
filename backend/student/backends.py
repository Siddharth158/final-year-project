from django.contrib.auth.backends import ModelBackend
from student.models import Student

class USNAuthBackend(ModelBackend):
    def authenticate(self, request, usn=None, password=None, **kwargs):
        try:
            user = Student.objects.get(usn=usn)
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except Student.DoesNotExist:
            return None
    def get_user(self, user_id):
        try:
            return Student.objects.get(pk=user_id)
        except Student.DoesNotExist:
            return None