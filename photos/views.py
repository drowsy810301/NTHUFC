# coding=utf-8

from django.shortcuts import render
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import get_object_or_404
from .socialApplication import uploadPhoto, getPhotoDetails, postComment, postLike, getHasLiked
from .models import Photo

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
		photo_id_list = [ int(x.id) for x in Photo.objects.all() ]
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
