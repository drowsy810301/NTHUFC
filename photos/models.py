#coding=utf-8

from django.db import models
from django.utils import timezone
from django.conf import settings
from locationMarker.models import Marker
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.validators import RegexValidator

from users.models import Account
from .authorization_token import fb_fanpage_graph
import os, re

# Create your models here.
class Tag(models.Model):

    tag_name = models.CharField(max_length=20, unique=True)
    tag_count = models.IntegerField(default=1)
    update_time = models.DateTimeField(default=timezone.now, blank=False)
    def __unicode__(self):
        return self.tag_name

    #比較某個詞跟這個標籤相似性
    def similarity(self, word):
        score = 0
        print type(self.tag_name)
        print type(word)
        uni_tag = self.tag_name
        uni_word = word
        for i in range(1,len(uni_word)+1):
            if i > len(uni_tag):
                continue
            for j in range(len(uni_word)-i+1):
                if uni_tag.find(uni_word[j:j+i]) > -1:
                    score += i
        return score

def getDefaultMarker():
    if len(Marker.objects.all()) == 0 :
        Marker.objects.create(title='清華大學', latitude=24.7913341, longitude=120.994148)
    return Marker.objects.all()[0].id;

def getFilePath(instance, filname):
    timeStr = str(timezone.now())
    return os.path.join('uploads','images',re.sub('\W','_',timeStr))

class Photo(models.Model):

    title = models.CharField(max_length=30)
    content = models.TextField(default=None, blank=True, null=True)
    #related_name can reverse foreign krey to one-to-many
    owner = models.ForeignKey(Account, related_name='photos')
    tags = models.CharField(max_length=32, default='tag1', validators=[RegexValidator(regex='^[^ ]{1,10}( [^ ]{1,10}){0,2}$',message='You can only enter at most 3 tags and seperate any 2 tags with a space.')])
    location_marker = models.ForeignKey(Marker, default=getDefaultMarker)
    flickr_photo_id = models.CharField(max_length=50, blank=True)
    flickr_photo_url = models.URLField(max_length=100, blank=True)
    facebook_post_id = models.CharField(max_length=50, blank=True)
    favorites = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    votes = models.IntegerField(default=0)
    upload_time = models.DateTimeField(default=timezone.now, blank=False, null=False)
    image = models.ImageField(upload_to=getFilePath, blank=True, null=True)
    isReady = models.BooleanField(default=False)
    last_modified_time = models.DateTimeField(default=timezone.now)
    #score of the photo description
    rank = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title

    def admin_thumbnail(self):
        if self.isReady:
            return u'<img src="{}" height="150px"/>'.format(self.flickr_photo_url)
        else:
            return u'<img src="{}" height="150px"/>'.format(self.image.url)
    admin_thumbnail.short_description = '相片預覽'
    admin_thumbnail.allow_tags = True

    def save(self, *args, **kwargs):
        try:
            self.clean()
            super(Photo,self).save(*args, **kwargs)
        except ValidationError as e :
            print str(e)

    def clean(self):
        if self.isReady:
            if not self.facebook_post_id or not self.flickr_photo_id or not self.flickr_photo_url:
                raise ValidationError({
                    'facebook_post_id': 'facebook_post_id is required',
                    'flickr_photo_id': 'flickr_photo_id is required',
                    'flickr_photo_url': 'flickr_photo_url is required',
                })
        else:
            if not self.image:
                raise ValidationError({'image': 'image file is required'})


class ReportedComment(models.Model):
    facebook_comment_id = models.CharField(max_length=50)
    facebook_post_url = models.CharField(max_length=100)
    name = models.CharField(max_length=20)
    message = models.CharField(max_length=200)
    report_count = models.IntegerField(default=0)
    report_list = models.CharField(max_length=200)
    last_report_time = models.DateTimeField(default=timezone.now)

    def delete(self, *args, **kwargs):
        fb_fanpage_graph.delete_object(id=self.facebook_comment_id)
        super(ReportedComment,self).delete(*args, **kwargs)

