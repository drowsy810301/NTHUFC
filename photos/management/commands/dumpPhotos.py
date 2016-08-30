#coding=utf-8

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from photos.socialApplication import uploadPhoto
from photos.models import Photo

class  Command(BaseCommand):
	help = 'upload unready photos to facebook and flickr'

	def handle(self, *args, **options):
		for photo in Photo.objects.filter(isReady=True):
			owner = photo.owner
			if owner.major =='':
				major = u'未填寫'
			else:
				major =owner.major

			print u'id={} {}:"{}" <{}({}) {} {} {} 手機={}> tags="{}" 地點={} flickr_photo_id={} [votes={} favorites={} likes={}] rank={}\n'.format(
					photo.id,
					photo.title,
					photo.content,
					owner.username,
					owner.nickname,
					owner.get_identity_display(),
					major,
					owner.email,
					owner.cellphone,
					photo.tags,
					photo.location_marker.title,
					photo.flickr_photo_id,
					photo.votes,
					photo.favorites,
					photo.likes,
					photo.rank,
				)