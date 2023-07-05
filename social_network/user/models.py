from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CustomUserModel(AbstractUser):
    last_activity = models.DateTimeField(_('last activity'), default=timezone.now)
