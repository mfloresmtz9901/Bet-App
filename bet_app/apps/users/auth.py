from django.conf import settings
from django.contrib.auth import get_user_model

from jose import jwt, JWTError
from ninja.security import APIKeyCookie

User = get_user_model()


class JWTAuthRequired(APIKeyCookie):
    param_name = settings.JWT_AUTH_COOKIE_NAME

    def authenticate(self, request, token):
        if not token:
            return None
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
            if user_id is None:
                return None
            return User.objects.get(id=user_id)
        except (JWTError, User.DoesNotExist):
            return None


jwt_auth = JWTAuthRequired()
