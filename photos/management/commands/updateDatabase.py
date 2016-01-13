from django.core.management.base import BaseCommand,CommandError
from django.utils import timezone
import time

from photos.socialApplication import getVotes
from photos.models import Photo

class Command(BaseCommand):
    def handle(self, *args, **options):
    	while True:
        	for photo in Photo.objects.all():
        		delta = timezone.now() - photo.last_modified_time
        		if delta.seconds >= 300:
	        		message = u'{} : {}'.format(photo.title,getVotes(photo))
	        		self.stdout.write(message)

