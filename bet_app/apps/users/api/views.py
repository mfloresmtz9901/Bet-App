from django.conf import settings
from django.db.models import QuerySet
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.security import SessionAuth

from bet_app.apps.users.api.schema import LoginSchema
from bet_app.apps.users.api.schema import RegisterSchema
from bet_app.apps.users.api.schema import UpdateUserSchema
from bet_app.apps.users.api.schema import UserSchema
from bet_app.apps.users.api.schema import UserOutSchema
from bet_app.apps.users.api.auth import create_access_token
from bet_app.apps.users.api.auth import jwt_auth
from bet_app.apps.users.models import User
from bet_app.apps.users.schemas import PasswordChangeInSchema

router = Router(tags=["users"])


def _get_users_queryset(request) -> QuerySet[User]:
    return User.objects.filter(pk=request.user.pk)


def set_auth_cookie(response: JsonResponse, token: str):
    response.set_cookie(
        key="bet_access_token",
        value=token,
        httponly=True,
        secure=False,  # Toggle to True in staging/production (Requires HTTPS)
        samesite="Lax",
        max_age=3600  # 1 Hour
    )


@router.post("/register", auth=[], response={201: UserOutSchema, 400: dict})
def register_user(request, data: RegisterSchema):
    if User.objects.filter(email=data.email).exists():
        return 400, {"message": "A user with this email already exists."}
    if User.objects.filter(username=data.username).exists():
        return 400, {"message": "A user with this username already exists."}

    user = User.objects.create_user(
        email=data.email, password=data.password, name=data.name, username=data.username)
    token = create_access_token(user.id)
    response = JsonResponse(UserOutSchema.from_orm(user).dict(), status=201)
    set_auth_cookie(response, token)
    return response


@router.post("/login/", auth=[])
def login_user(request, data: LoginSchema):
    try:
        user = User.objects.get(email=data.email)
    except User.DoesNotExist:
        return JsonResponse({"detail": "Invalid credentials"}, status=401)
    if not user.check_password(data.password):
        return JsonResponse({"detail": "Invalid credentials"}, status=401)

    token = create_access_token(user.id)
    response = JsonResponse({"message": "Login successful"})
    response.set_cookie(
        key=settings.JWT_AUTH_COOKIE_NAME,
        value=token,
        httponly=True,
        secure=False,
        samesite="Lax",
        max_age=3600,
    )
    return response


@router.get("/", response=list[UserSchema])
def list_users(request):
    return _get_users_queryset(request)


@router.get("/me/", response=UserSchema, auth=[SessionAuth(), jwt_auth])
def retrieve_current_user(request):
    return request.auth


@router.get("/{username}/", response=UserSchema)
def retrieve_user(request, username: str):
    users_qs = _get_users_queryset(request)
    return get_object_or_404(users_qs, username=username)


@router.patch("/me/", response=UserSchema)
def update_current_user(request, data: UpdateUserSchema):
    user = request.user
    user.name = data.name
    user.username = data.username
    user.save()
    return user


@router.patch("/{username}/", response=UserSchema)
def update_user(request, username: str, data: UpdateUserSchema):
    users_qs = _get_users_queryset(request)
    user = get_object_or_404(users_qs, username=username)
    user.name = data.name
    user.username = data.username
    user.save()
    return user


@router.post("/change-password", auth=jwt_auth, response={200: dict, 400: dict})
def change_password(request, data: PasswordChangeInSchema):
    user = request.auth
    if not user.check_password(data.old_password):
        return 400, {"message": "Your current password verification failed."}

    user.set_password(data.new_password)
    user.save()
    return 200, {"success": True, "message": "Password updated successfully."}
