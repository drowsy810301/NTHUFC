from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from photos.socialApplication import uploadPhoto
from photos.models import Photo

class  Command(BaseCommand):
	help = 'upload unready photos to facebook and flickr'

	def handle(self, *args, **options):
		for p in Photo.objects.filter(isReady=False):
			uploadPhoto(p)