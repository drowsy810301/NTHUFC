#-*- encoding=UTF-8 -*-
from django import forms

class FeedbackForm(forms.Form):
	type_choice = (
		('SUGGEUST','網站設計建議'),
		('BUG','錯誤回報'),
		('MARKER','發現清華秘境'),
	)
	email = forms.EmailField(label='信箱', max_length=50)
	type = forms.ChoiceField(label='類別', choices=type_choice)
	message = forms.CharField(label='訊息', max_length=200, widget=forms.Textarea)