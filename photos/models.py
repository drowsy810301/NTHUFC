#coding=utf-8

from django.db import models
from django.utils import timezone
from django.conf import settings
from users.models import Account
from locationMarker.models import Marker
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.validators import RegexValidator
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
    content = models.TextField(default=None)
    #related_name can reverse foreign krey to one-to-many
    owner = models.ForeignKey(Account, related_name='photos')
    tags = models.CharField(max_length=32, default='tag1',validators=[RegexValidator(regex='^[^ ]{1,10}( [^ ]{1,10}){0,2}$',message='You can only enter at most 3 tags and seperate any 2 tags with a space.')])
    location_marker = models.ForeignKey(Marker, default=getDefaultMarker)
    flickr_photo_id = models.CharField(max_length=50,blank=True)
    flickr_photo_url = models.URLField(max_length=100,blank=True)
    facebook_post_id = models.CharField(max_length=50,blank=True)
    upload_time = models.DateTimeField(default=timezone.now, blank=False, null=False)
    image = models.ImageField(upload_to=getFilePath)
    isReady = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title

    def getTagString(self):
        tagString = ''
        for tag in self.tags:
            tagString += tag.tag_name;
        return tagString;

    def delete(self, *args, **kwargs):
        for tag_text in self.tags.split(' '):
            if tag_text == '':
                continue
            try:
                tag = Tag.objects.get(tag_name = tag_text)
                tag.tag_count -= 1
                tag.save()
            except ObjectDoesNotExist:
                pass

        super(Photo,self).delete(*args, **kwargs)



class WorkerManager(models.Manager):
    def create(self,*args,**kwargs):
        book = super(WorkerManager,self).create(*args,**kwargs)
        print 'creating...'
        return book

class Worker(models.Model):
    name = models.CharField(max_length=5)
    objects = WorkerManager()
    def save(self,*args,**kwargs):
        print 'saving...'
        super(Worker,self).save(*args,**kwargs)

    def delete(self,*args,**kwargs):
        print 'deleting...'
        super(Worker,self).delete(*args,**kwargs)