from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

class DebugJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        raw_token = self.get_raw_token(header)

        if raw_token is None:
            print("No token found in the request headers.")
            return None

        # print(f"Raw token received: {raw_token}")  # Debug: Log the raw token

        try:
            validated_token = self.get_validated_token(raw_token)
            # print(f"Validated token: {validated_token}")
            # print("Decoded Token:", validated_token.payload)# Debug: Log the validated token
        except Exception as e:
            print(f"Token validation failed: {e}")  # Debug: Log validation errors
            return None

        user = self.get_user(validated_token)
        if user is None:
            print("No user resolved from the validated token.")
        else:
            print(f"Resolved user: {user}")  # Debug: Log the authenticated user
        return user, validated_token
