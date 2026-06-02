from datetime import datetime, timedelta, timezone

from django.conf import settings
from django.contrib.auth import get_user_model

from jose import JWTError, jwt
from ninja.security import APIKeyCookie

User = get_user_model()


def create_access_token(user_id: int) -> str:
    expire = datetime.now(tz=timezone.utc) + timedelta(hours=1)
    payload = {"user_id": user_id, "exp": int(expire.timestamp())}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


class JWTAuthRequired(APIKeyCookie):
    param_name = settings.JWT_AUTH_COOKIE_NAME

    def authenticate(self, request, token):
        if not token:
            return None
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
            if user_id is None:
                return None
            return User.objects.get(id=user_id)
        except (JWTError, User.DoesNotExist):
            return None


jwt_auth = JWTAuthRequired()
