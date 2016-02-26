from django.contrib import admin
from .models import Feedback
# Register your models here.


class FeedbackAdmin(admin.ModelAdmin):
	list_display = ('label', 'message', 'email', 'update_date', 'is_solved')
	ordering = ['is_solved' ,'-update_date']

admin.site.register(Feedback, FeedbackAdmin)