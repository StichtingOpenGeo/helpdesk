import re, unicodedata

from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext
from django.conf import settings
from django.contrib.auth.models import User

class SignupQueue(models.Model):
    # Data for generating signup
    email = models.EmailField(_('Email address'), unique=True)
    name = models.CharField(_('Name (representative)'), max_length=75)
    position = models.CharField(_('Position'), max_length=100, blank=True)
    organization = models.CharField(_('Organization name'), max_length=100, blank=True)
    city = models.CharField(_('City'), max_length=50)

    # Uploaded signup
    signed_file = models.FileField(upload_to=getattr(settings, 'SIGNUP_UPLOAD_TO', settings.MEDIA_ROOT), blank=True)

    # Track progress
    STATUSES = ((1, _('Request')),
                (2, _('Generated')),
                (3, _('Uploaded')),
                (4, _('Verified')),
                )
    status = models.IntegerField(_('Status'), default=1, choices=STATUSES)
    date_requested = models.DateField(auto_now_add=True)
    date_uploaded = models.DateField(blank=True, null=True)
    date_verified = models.DateField(blank=True, null=True)

    # Once we create a user, link it to the registration
    user = models.ForeignKey(User, blank=True, null=True)

    class Meta:
        verbose_name = _("registration")

    def __unicode__(self):
      return u'%s - %s'  % (self.name, self.organization)

    def create_user(self):
      ''' Create a new account with a random password and make sure we have a unique username '''
      if self.user is not None:
        return (self.user.username, None)


      password = User.objects.make_random_password()
      # Remove anything not a word character/letter or is a decimal
      username = unicodedata.normalize('NFKD', self.name.lower()) # Remove accents first
      regex = re.compile(r'[\W\d]', re.UNICODE) # Unicode is needed for any remaining weird characters
      username = regex.sub('', username)

      # Generate a unique username, append a number if we can't
      suffix_number = 1
      while User.objects.filter(username__exact=username).count() > 0:
        username = "%s%i" % (username[:-1] if suffix_number > 1 else username, suffix_number)
        suffix_number += 1

      u = User.objects.create_user(username, self.email, password)

      # Link the user to the signup
      self.user = u
      self.save()
      return (username, password)