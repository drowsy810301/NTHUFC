#-*- encoding=UTF-8 -*-
from django import forms
from django.forms import ModelForm

from .models import Feedback

class FeedbackForm(ModelForm):
	class Meta:
		model = Feedback
		fields = [
			'email',
			'label',
			'message',
		]
