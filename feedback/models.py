#-*- encoding=UTF-8 -*-
from django.db import models
from django.utils import timezone
# Create your models here.

class Feedback(models.Model):
	LABEL_CHOICE = (
		('SUGGEUST','網站設計建議'),
		('BUG','錯誤回報'),
		('MARKER','發現清華秘境'),
	)

	email = models.EmailField()
	label = models.CharField( choices= LABEL_CHOICE, max_length=10 )
	message = models.TextField( max_length=512 )
	is_solved = models.BooleanField( default=False )
	update_date = models.DateTimeField( default=timezone.now)

	def __unicode__(self):
		return self.message