from django.contrib import admin
from photos.models import Photo, Tag, ReportedComment
from photos.socialApplication import uploadPhoto
# Register your models here.

def make_uploaded(modeladmin, request, queryset):
    for p in queryset:
    	if not p.isReady:
    		uploadPhoto(p)
make_uploaded.short_description = "Uploads photos"

def deletePhoto(modeladmin, request, queryset):
    for p in queryset:
    	p.delete();
deletePhoto.short_description = "Delete photos (customed)"

class PhotoAdmin(admin.ModelAdmin):
	list_display = ('id','title','content','tags','admin_thumbnail','isReady');
	ordering = ['isReady']
	actions = [make_uploaded,deletePhoto]

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

