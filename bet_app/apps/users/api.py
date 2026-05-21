from django.conf import settings
from django.contrib.auth import authenticate
from django.http import JsonResponse

from datetime import datetime, timedelta
from jose import jwt
from ninja import Router

from .auth import jwt_auth
from .schemas import LoginSchema, UserSchema

router = Router()


def create_access_token(user_id: int) -> str:
    expire = datetime.now() + timedelta(hours=1)
    to_encode = {"user_id": user_id, "expiration": expire.isoformat()}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm='HS256')


@router.post("/login")
def login(request, data: LoginSchema):
    user = authenticate(username=data.username, password=data.password)
    if not user:
        return JsonResponse({"error": "Invalid credentials"}, status=401)

    token = create_access_token(user.id)
    response = JsonResponse({"success": True, "message": "Login successfully"})

    response.set_cookie(
        key=settings.JWT_AUTH_COOKIE_NAME,
        value=token,
        httponly=True,
        secure=False,
        samesite='Lax',
        max_age=3600
    )
    return response

# test endpoint to verify authentication


@router.get('/me', auth=jwt_auth, response=UserSchema)
def get_current_user(request):
    return request.auth
