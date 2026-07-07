from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from src.apps.account.managers.account import UserManager
from src.apps.common.models import BaseModel, RoleChoice


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    email = models.EmailField(
        max_length=254,
        unique=True,
    )
    first_name = models.CharField(
        blank=True,
        max_length=150,
        verbose_name=_("first name"),
    )
    last_name = models.CharField(
        blank=True,
        max_length=150,
        verbose_name=_("last name"),
    )
    role = models.CharField(
        choices=RoleChoice.choices,
        default=RoleChoice.PLANNER,
        max_length=15,
    )
    is_active = models.BooleanField(
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. Unselect this instead of deleting account."
        ),
        verbose_name=_("active"),
    )

    is_staff = models.BooleanField(
        default=False,
        help_text=_(
            "Designates whether the user can log into this admin site.",
        ),
        verbose_name=_("staff status"),
    )
    is_superuser = models.BooleanField(
        default=False,
        verbose_name=_("superuser status"),
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("date joined"),
    )

    objects = UserManager()

    USERNAME_FIELD = "email"

    class Meta:
        ordering = ("-id",)
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.email
