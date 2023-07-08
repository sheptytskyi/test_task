from django.db import models
from uuid import uuid4
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class PostModel(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True, editable=False, unique=True)
    title = models.CharField(_('title'), max_length=256)
    content = models.TextField(_('content'))
    author = models.ForeignKey(
        verbose_name=_('author'),
        to=User,
        related_name='posts',
        on_delete=models.CASCADE,
        null=True
    )
    likes = models.ManyToManyField(
        User,
        verbose_name=_('likes'),
        through='LikePostModel',
        related_name='likes',
        null=True,
        blank=True
    )
    dislikes = models.ManyToManyField(
        User,
        verbose_name=_('dislikes'),
        through='DisLikePostModel',
        related_name='dislikes',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)

    class Meta:
        db_table = 'post'
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    def __str__(self) -> str:
        return f'{self.title}'

    @property
    def likes_count(self) -> int:
        return self.likes.all().count()

    @property
    def dislikes_count(self) -> int:
        return self.dislikes.all().count()


class LikePostModel(models.Model):
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.now)


class DisLikePostModel(models.Model):
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.now)
