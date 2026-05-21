from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Default custom user model for Bet App.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    email = models.EmailField(unique=True, max_length=255)

    USER_TYPE_CHOICES = [
        ("FR", _("Free")),
        ("PR", _("Premium")),
        ("AD", _("Admin")),
    ]
    user_type = models.CharField(
        max_length=2, null=True, blank=True, verbose_name=_("User Type"), choices=USER_TYPE_CHOICES
    )

    @property
    def is_platform_admin(self):
        """Helper property to identify platform admins."""
        return self.user_type == "AD"

    def __str__(self):
        return f"{self.email} ({'Admin' if self.user_type == 'AD' else 'User'})"
