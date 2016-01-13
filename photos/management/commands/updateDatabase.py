from django.core.management.base import BaseCommand,CommandError
from django.utils import timezone
import time
import gc

from photos.socialApplication import getVotes
from photos.models import Photo

class Command(BaseCommand):

    def handle(self, *args, **options):
    	delta = timezone.now()
    	gc_time = timezone.now()
    	while True:
        	for photo in Photo.objects.all():
        		delta = timezone.now() - photo.last_modified_time
        		if delta.seconds >= 300:
	        		self.stdout.write(u'{} : {}'.format(photo.title,getVotes(photo)))

	        delta = timezone.now() - gc_time
        	if delta.seconds >= 300:
        		gc_time = timezone.now()
	        	gc.collect()

