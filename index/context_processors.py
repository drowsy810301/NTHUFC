from photos.models import Photo
from users.models import Account

def count_processor(request):
  count = {}
  count['people'] = Account.objects.count()
  count['photo'] = Photo.objects.count()
  return {'count': count}
