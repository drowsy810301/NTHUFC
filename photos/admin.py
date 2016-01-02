from django.contrib import admin
from photos.models import Photo, Tag
# Register your models here.

class PhotoAdmin(admin.ModelAdmin):
	list_display = ('id','title');

class TagAdmin(admin.ModelAdmin):
	list_display = ('tag_name','tag_count');

admin.site.register(Photo,PhotoAdmin)
admin.site.register(Tag,TagAdmin)

