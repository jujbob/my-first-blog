from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core import validators
from django.core.files.base import ContentFile
from django.core.mail import send_mail
from django.db import models
from sorl.thumbnail import get_thumbnail


class AccountManager(BaseUserManager):

    def create_user(self, email, password=None, **kwargs):

        if not email:
            raise ValueError('Users must have a valid email')
        if not kwargs.get('username'):
            raise ValueError('Users have to have a name')

        account = self.model(
            email = self.normalize_email(email), is_superuser=False, username = kwargs.get('username')
        )

        account.set_password(password)
        account.save()

        return account

    def create_superuser(self, email, password=None, **kwargs):
        account = self.create_user(email, password, **kwargs)

        account.is_superuser = True
        account.is_admin = True
        account.is_staff = True
        account.save()

        return account




class Account(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(('username'), max_length=30, unique=False,
                                help_text=('Required. 30 characters or fewer. Letters, digits'
                                            ' and ./+/-/_ only.'),
                                error_messages={
                                    'invalid': "Username may contain only letters, numbers and "
                                               "@.+-_ characters."},
                                validators=[
                                    validators.RegexValidator(r'^[\w.+-]+$', ('Enter a valid username jebal.'), 'invalid')
                                ])

    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    tagline = models.CharField(max_length=150, blank=True)
    nation_code = models.CharField(max_length=50, blank=True)
    nation_name = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=50, blank=True)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    introduction = models.TextField(blank=True)
    content = RichTextField(blank=True)

    objects = AccountManager()

    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'

    def __unicode__(self):
        return self.email

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def get_short_name(self):
        return self.first_name

    @property
    def user_image_url(self):
        # Pseudocode:

        if self.user_image.count() >= 1:
            return self.user_image.last().user_image
        else:
            return "image/profile/default_profile.jpg"


    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

class UserImage(models.Model):

    user = models.ForeignKey('authentication.Account', related_name='user_image')
    user_image = models.ImageField(upload_to='image/profile/%Y/%m/%d', blank=True,)

    def save(self, *args, **kwargs):

        if not self.id:
            super(UserImage, self).save(*args, **kwargs)
            standard_width = 500
            standard_height = 500
            result_size = str(standard_width)+'x'+str(standard_height)
            resized = get_thumbnail(self.user_image, result_size, quality=90, format='JPEG')
            self.user_image.save(resized.name, ContentFile(resized.read()), True)
        super(UserImage, self).save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        self.user_image.delete()
        super(UserImage, self).delete(*args, **kwargs)