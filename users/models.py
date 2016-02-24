#-*- encoding=UTF-8 -*-
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from  django.contrib.auth.hashers import make_password
from datetime import date, datetime, timedelta
# Create your models here.

def get_default_active_time():
    return datetime.now() + timedelta(minutes=15)


class Account(models.Model):
    username = models.CharField(max_length=20, default='', unique=True)
    nickname = models.CharField(max_length=20, default='')

    TEACHER = 'TE'
    STUDENT = 'ST'
    OFFICER = 'OF'
    ALUMNUS = 'AL'
    IDENTITY_CHOICES = (
        (ALUMNUS, '校友'),
        (OFFICER, '職員'),
        (STUDENT, '學生'),
        (TEACHER, '教師')
    )

    ADMIN = 'ADMIN'
    JUDGE = 'JUDGE'
    USER = 'USER'
    USER_LEVEL_CHOICE = (
        (ADMIN, 'Admin'),
        (JUDGE, 'Judge'),
        (USER, 'User'),
    )
    is_staff = models.BooleanField(default=False)
    identity = models.CharField(max_length=2, choices=IDENTITY_CHOICES, default=None)
    major = models.CharField(max_length=20, default='', blank=True, null=True)
    email = models.EmailField(max_length=250, unique=True)
    cellphone = models.CharField(max_length=10, unique=True, validators=[RegexValidator(regex='^\d{10}$', message='Invalid number', code='Invalid number')])
    #ID_card = models.CharField(max_length=10, unique=True, validators=[RegexValidator(regex='^([A-Z][12]\d{8})$', message='Invalid id number', code='Invalid id number')])
    password = models.CharField(max_length=80, blank = False)
    #score of photos description
    photos_rank = models.FloatField(default=0)
    user_level = models.CharField(max_length=9, choices=USER_LEVEL_CHOICE, default=USER)
    is_agree = models.BooleanField(default=False)



    def __unicode__(self):
        return self.username

    def updatePhotosRank(self):
        count = 0
        rank_sum = 0
        for photo in self.photos.all():
            rank_sum += photo.rank
            count += 1
        if count > 0:
            self.photos_rank = 1.0*rank_sum/count
        else:
            self.photos_rank = 0

        self.save(update_fields=['photos_rank'])

    def save(self, *args, **kwargs):
        if self.password:
            self.password = make_password(self.password)
        super(Account, self).save(*args, **kwargs)
    
    def reset_password(self, raw_password, *args, **kwargs):
        self.password = make_password(raw_password) 
        super(Account, self).save(*args, **kwargs)

    '''custom authentication resolve 'is_authenticated' problem'''
    def is_authenticated(self):
        return True

    @property
    def is_superuser(self):
        return self.is_admin

    def is_active(self):
        return True

    def is_admin(self):
        return False

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    def has_judge_auth(self):
        has_auth = ((self.user_level == self.ADMIN) or (self.user_level == self.JUDGE))
        return has_auth

class UserProfile(models.Model):
    account = models.OneToOneField(Account)
    activation_key = models.CharField(max_length=40, blank=True)
    # default active time is 15 minutes
    active_time = models.DateTimeField(default=get_default_active_time)

    def __unicode__(self):
        return self.account.username

    class Meta:
        verbose_name_plural=u'Account profiles'
