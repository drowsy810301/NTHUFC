from django.core.management.base import BaseCommand,CommandError
from django.utils import timezone
import time

from photos.socialApplication import getVotes
from photos.models import Photo

class Command(BaseCommand):

    def handle(self, *args, **options):
    	delta = timezone.now()
        for photo in Photo.objects.filter(isReady=True):
        	delta = timezone.now() - photo.last_modified_time
        	if delta.seconds >= 300:
	       		self.stdout.write(u'{} : {}'.format(photo.title,getVotes(photo)))

