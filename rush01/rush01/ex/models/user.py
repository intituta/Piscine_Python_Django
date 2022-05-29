from ex.models.comment import CommentModel
from ex.models.post import PostModel
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils import timezone
from django.dispatch import receiver
from uuid import uuid4
import os


class UserManager(BaseUserManager):
    def create_user(self, id, email, password=None):
        if not id:
            raise ValueError('Users must have an id')

        if not email:
            raise ValueError('Users must have an email')

        user = self.model(
            id=id,
            email=self.normalize_email(email),
            name="",
            surname="",
            description=""
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, id, email, password):
        user = self.create_user(
            id=id,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


def path_and_rename(instance, filename):
    upload_to = 'profile'
    ext = filename.split('.')[-1]
    if instance.pk:
        filename = '{}-{}.{}'.format(instance.id, timezone.now(), ext)
    else:
        filename = '{}-{}.{}'.format(uuid4().hex, timezone.now(), ext)
    return os.path.join(upload_to, filename)


class User(AbstractBaseUser):
    id = models.CharField(max_length=64, primary_key=True, unique=True, null=False)
    email = models.EmailField(max_length=128, unique=True, null=False)
    name = models.CharField(max_length=64, blank=True, null=False)
    surname = models.CharField(max_length=64, blank=True, null=False)
    description = models.TextField(max_length=512, blank=True, null=False)
    profile_image = models.ImageField(
        upload_to=path_and_rename, blank=True, null=False)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = [
        'email',
    ]

    def __str__(self):
        return self.id

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_post_count(self):
        return PostModel.objects.filter(author=self,is_active=True).count()

    def get_comment_count(self):
        return CommentModel.objects.filter(author=self,is_active=True).count()

    @property
    def is_staff(self):
        return self.is_admin


@receiver(models.signals.post_delete, sender=User)
def auto_delete_file_on_delete(sender, instance: User, **kwargs):
    if instance.profile_image:
        if os.path.isfile(instance.profile_image.path):
            os.remove(instance.profile_image.path)


@receiver(models.signals.pre_save, sender=User)
def auto_delete_file_on_change(sender, instance: User, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).profile_image
    except sender.DoesNotExist as e:
        return False
    if not old_file:
        return True
    new_file = instance.profile_image
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
