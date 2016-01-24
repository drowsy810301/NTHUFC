# coding=utf-8

from django.shortcuts import render
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import get_object_or_404
from .socialApplication import uploadPhoto, getPhotoDetails, postComment, postLike, getHasLiked, getVotes,getPhotoModalDetails
from .models import Photo, Tag
from locationMarker.models import Marker
from users.models import Account

# Create your views here.
def photos(request):
    return render(request, "photos/photos.html", {})

'''
def upload(request,photo_id):
	photo = get_object_or_404(Photo,pk=photo_id)
	response = uploadPhoto(photo)
	return render(request, "photos/upload.html", {'response':response})
'''

#ajax需要csrf_token來驗證
@ensure_csrf_cookie
def show(request):
	if request.method == 'POST':
		print request.POST
		photo_list = []
		for id in request.POST.getlist('photo_id_list[]'):
			try:
				photo_list.append(Photo.objects.get(pk=id))
			except ObjectDoesNotExist:
				pass
			except Exception , e:
				return JsonResponse({'status':'error', 'message':str(e)})

		user_access_token = request.POST.get('user_access_token','')
		return JsonResponse({'photo_list':[getPhotoDetails(x,user_access_token) for x in photo_list]})
	else:
		photo_id_list = [ x.id for x in Photo.objects.all() ]
		return render(request,"photos/show.html",{'photo_id_list':photo_id_list})

def ajax_post_comment(request):
	access_token = request.POST.get('access_token','')
	photo_facebook_id = request.POST.get('photo_facebook_id','')
	comment_text = request.POST.get('comment_text','')

	if access_token == '' or photo_facebook_id=='' or comment_text=='':
		return JsonResponse({'status':'error', 'message':'post data missing'})
	else:
		return JsonResponse({'photo_facebook_id':photo_facebook_id, 'comment_list': postComment(access_token,photo_facebook_id,comment_text)})

def ajax_post_like(request):

	user_access_token = request.POST.get('access_token','')
	#按 photo_facebook_id 的讚
	photo_facebook_id = request.POST.get('photo_facebook_id','')
	photo_list = request.POST.getlist('photo_list[]')

	if user_access_token == '':
		return JsonResponse({'status':'error', 'message':'access_token missing'})
	else:
		context={}
		if photo_facebook_id !='':
			context['facebook_likes'] = postLike(user_access_token,photo_facebook_id)
			context['flickr_likes'] = Photo.objects.get().flickr_likes

		hasLiked_list = []
		for id in  photo_list:
			try:
				tmp_photo_facebook_id = Photo.objects.get(pk=id).facebook_post_id
				if getHasLiked(tmp_photo_facebook_id, user_access_token):
					hasLiked_list.append(tmp_photo_facebook_id)
			except ObjectDoesNotExist:
				pass
		context['hasLiked_list'] = hasLiked_list
		return JsonResponse(context)

@ensure_csrf_cookie
def vote(request):
	all_account = Account.objects.order_by('-photos_rank')
	data_list = []
	for account in all_account:
		account_data = {}
		all_photos = account.photos.filter(isReady=True).order_by('-votes')
		if not all_photos:
			continue
		account_data['nickname'] = account.nickname
		account_data['photo_list'] = []
		for photo in all_photos:
			account_data['photo_list'].append({
				'votes': photo.likes+photo.favorites,
				'facebook_post_id':photo.facebook_post_id,
				'flickr_link':'https://www.flickr.com/photos/138506275@N05/'+photo.flickr_photo_id,
				'img_src':photo.flickr_photo_url,
			})
		data_list.append(account_data)
	return render(request,'photos/vote.html',{'data_list':data_list})

def ajax_get_votes(request):
	if request.method == 'POST' and 'facebook_post_id' in request.POST:
		facebook_post_id = request.POST['facebook_post_id']
		photo = Photo.objects.get(facebook_post_id=facebook_post_id)
		return JsonResponse({'votes': getVotes(photo)})

def photo_map(request):
	all_tags = Tag.objects.all()
	hot_tags = Tag.objects.order_by('-tag_count')[:3]
	recent_tags = Tag.objects.order_by('-update_time')[:3]
	return render(request,'photos/photo_map.html',{
		"marker_list": Marker.objects.all(),
        "all_tags":[ x.tag_name for x in all_tags],
        "hot_tags":[ x.tag_name for x in hot_tags],
        "recent_tags":[ x.tag_name for x in recent_tags],
	})

def ajax_get_photo_details(request):
	if request.method == 'POST' and 'facebook_post_id' in request.POST:
		facebook_post_id = request.POST['facebook_post_id']
		photo = Photo.objects.get(facebook_post_id=facebook_post_id)

		return JsonResponse({'photo': getPhotoModalDetails(photo) })

