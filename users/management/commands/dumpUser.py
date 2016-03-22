#coding=utf-8

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from photos.socialApplication import uploadPhoto
from photos.models import Photo
from users.models import Account

class  Command(BaseCommand):
	help = 'dump all contest participants'

	def handle(self, *args, **options):
		count = 0
		for u in Account.objects.all():
			photo_list = u.photos.all()
			photo_id_list = ''
			if len( photo_list ) == 0:
				continue
			else:
				for p in photo_list:
					photo_id_list += ' {},'.format(p.id)			
			count += 1
			if u.major == '':
				u.major = u'未填寫major'
			print u'{}({})\t\t{}\t{}\t{}\t{}\t上傳了{}張照片({})'.format( u.username, u.nickname, u.get_identity_display(), u.major, u.email, u.cellphone, len(photo_list), photo_id_list )
		print 'total {} users'.format(count)
