from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import mail_admins
from django.core.urlresolvers import reverse
from django.conf import settings

import threading

from .models import Feedback
from .forms import FeedbackForm
# Create your views here.

def ajax_send_feedback(request):
	class SendMailThread(threading.Thread):
		def run(self):
			mail_admins('Too many unread feedbacks', 'There are too many unread feedbacks, please solve them as soon as possible!\nLink: '+settings.DOMAIN_NAME+reverse('admin:feedback_feedback_changelist'))

	if request.method=='POST':
		form = FeedbackForm(request.POST)
		if form.is_valid():
			form.save()
			if Feedback.objects.filter(is_solved =False).count()>=5 :
				SendMailThread().start()
			return JsonResponse({'status':'success'})

	return JsonResponse({'error':form.errors})
