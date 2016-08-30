#coding=utf-8

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from photos.socialApplication import uploadPhoto
from photos.models import Photo

class  Command(BaseCommand):
	help = 'upload unready photos to facebook and flickr'

	def handle(self, *args, **options):
		for photo in Photo.objects.filter(isReady=True):
			print u'{}:{}\n'.format(
					photo.flickr_photo_id,
					photo.title,
				)
