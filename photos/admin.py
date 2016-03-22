from django.contrib import admin
import threading

from photos.models import Photo, Tag, ReportedComment
from photos.socialApplication import uploadPhoto, deletePhoto
# Register your models here.

def make_uploaded(modeladmin, request, queryset):
	class MyUploadPhotoThread(threading.Thread):
		def __init__(self, queryset):
			super( MyUploadPhotoThread, self).__init__()
			self.queryset = queryset

		def run(self):
			for p in self.queryset:
				uploadPhoto(p)

	MyUploadPhotoThread(queryset).start()

make_uploaded.short_description = "Uploads photos"

def myDeletePhoto(modeladmin, request, queryset):
	for p in queryset:
		deletePhoto(p)
myDeletePhoto.short_description = "Delete photos (customed)"

class PhotoAdmin(admin.ModelAdmin):
	#list_display = ('id','title','content','tags','admin_thumbnail','isReady');
	list_display = ('id','title','owner','location_marker','flickr_photo_id','votes','favorites','likes','rank','isReady');
	ordering = ['isReady']
	actions = [myDeletePhoto]

class TagAdmin(admin.ModelAdmin):
	list_display = ('tag_name','tag_count');


def delete_comment(modeladmin, request, queryset):
	for comment in queryset:
		comment.delete()
delete_comment.short_description = "Delete from Facebook"

class ReportedCommentAdmin(admin.ModelAdmin):
	list_display = ('message', 'facebook_post_url', 'report_count')
	ordering = ['report_count']
	actions = [ delete_comment ]

admin.site.register(Photo, PhotoAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(ReportedComment, ReportedCommentAdmin)

