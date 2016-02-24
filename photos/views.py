# coding=utf-8

from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings
from django.utils import timezone
from django.core.mail import mail_admins
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.db.models import Count

import threading
import math

from .socialApplication import getPhotoDetails, postComment, postLike, getHasLiked, getVotes,getPhotoModalDetails, getFlickrAuthorizationUrl,changeFlickrFavorite, getFlickrAccessToken
from .models import Photo, Tag, ReportedComment
from locationMarker.models import Marker
from users.models import Account
from flickr_api.flickrerrors import FlickrAPIError

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
def vote(request, page=1):
	shared_photo = None
	shared_photo_id = None
	shared_photo_owner_id = None

	valid_accounts =  Account.objects.annotate(n_photo = Count('photos')).filter(n_photo__gt=0)
	all_page = int( math.ceil(1.0* valid_accounts.count() /5) )
	if request.method == 'GET':
		try:
			page = int(page)
			if page <= 0 or page > all_page:
				raise Exception
		except:
			page = 1

	if ( request.method == 'GET' and 'photo_id' in request.GET ):
		try:
			shared_photo = Photo.objects.get(pk=request.GET['photo_id'])
			if shared_photo.isReady:
				shared_photo_id = shared_photo.id
				shared_photo_owner_id = shared_photo.owner.id
				page = 1
		except ( ValueError, ObjectDoesNotExist) as e:
			pass

	if shared_photo_owner_id:
		all_account = list(Account.objects.filter(pk=shared_photo_owner_id)) + list(valid_accounts.exclude(pk=shared_photo_owner_id).order_by('-photos_rank'))
	else:
		all_account = list(valid_accounts.order_by('-photos_rank'))

	all_account = all_account[5*(page-1):5*page]

	data_list = []
	for account in all_account:
		account_data = {}
		if shared_photo_id and shared_photo_owner_id == account.id :
			all_photos = list(account.photos.filter(isReady=True,pk=shared_photo_id)) + list(account.photos.filter(isReady=True).exclude(pk=shared_photo_id).order_by('-votes'))
		else:
			all_photos = list(account.photos.filter(isReady=True).order_by('-votes'))
		if not all_photos:
			continue
		account_data['nickname'] = account.nickname
		account_data['photo_list'] = []
		for photo in all_photos:
			account_data['photo_list'].append({
				'votes': photo.likes+photo.favorites,
				'facebook_post_id':photo.facebook_post_id,
				'flickr_photo_id':photo.flickr_photo_id,
				'img_src':photo.flickr_photo_url,
			})
		data_list.append(account_data)

	if shared_photo_owner_id and shared_photo_id:
		return render(request,'photos/vote.html',{'data_list':data_list, 'all_page': all_page, 'page' : page, 'shared_photo_facebook_post_id': shared_photo.facebook_post_id})
	else:
		return render(request,'photos/vote.html',{'data_list':data_list, 'all_page': all_page, 'page' : page, })

def ajax_get_votes(request):
	if request.method == 'POST' and 'facebook_post_id' in request.POST:
		facebook_post_id = request.POST['facebook_post_id']
		photo = Photo.objects.get(facebook_post_id=facebook_post_id)
		return JsonResponse({'votes': getVotes(photo)})

def ajax_get_photo_details(request):
	if request.method == 'POST' and 'facebook_post_id' in request.POST:
		facebook_post_id = request.POST['facebook_post_id']
		try:
			photo = Photo.objects.get(facebook_post_id=facebook_post_id)
			report_list = request.session.get('report_comment_list',[])
			return JsonResponse({'photo': getPhotoModalDetails(photo, report_list) })
		except ObjectDoesNotExist:
			return redirect('index:index')
	else:
		return redirect('index:index')

def flickr_authorization_redirect(request, flickr_photo_id, facebook_post_id):
	if (request.method == 'GET'):
		if ( 'access_key' in request.session and 'access_secret' in request.session ):
			return render(request,'photos/flickr_authorization_redirect.html', { 'flickr_photo_id':flickr_photo_id, 'facebook_post_id':facebook_post_id, })
		elif ( 'oauth_verifier' in request.GET and  'request_key' in request.session and  'request_secret' in request.session):
			[access_key,access_secret] = getFlickrAccessToken(str(request.session['request_key']),str(request.session['request_secret']), str(request.GET['oauth_verifier']) )
			del request.session['request_key']
			del request.session['request_secret']
			request.session['access_key'] = access_key
			request.session['access_secret'] = access_secret

			return render(request,'photos/flickr_authorization_redirect.html', { 'flickr_photo_id':flickr_photo_id, 'facebook_post_id':facebook_post_id, })
		else:
			return render(request,'photos/flickr_authorization_redirect.html')

	return redirect('photos:vote');

def ajax_post_flickr_favorite(request):
	if (request.method == 'POST' and 'flickr_photo_id' in request.POST and 'facebook_post_id' in request.POST ):
		method = request.POST.get('method', 'ADD')
		if ( 'access_key' in request.session and 'access_secret' in request.session ):
			try:
				changeFlickrFavorite(str(request.session['access_key']), str(request.session['access_secret']), str(request.POST['flickr_photo_id']) , method)
				return JsonResponse( { 'status':'ok', 'method':method } )
			except FlickrAPIError as e:
				if (method == 'ADD' and e.code == 3) or (method == 'DELETE' and e.code == 1):
					return JsonResponse( { 'status':'ok', 'method':method ,'message':e.message } )
				else:
					return JsonResponse( { 'status':'error' , 'code': e.code , 'message':e.message } )
		else:
			[url,request_key,request_secret] = getFlickrAuthorizationUrl( request.POST['flickr_photo_id'], request.POST['facebook_post_id'] )
			request.session['request_key'] = request_key
			request.session['request_secret'] = request_secret
			return JsonResponse( { 'status': 'notLogin', 'auth_url': url} );
	else:
		return JsonResponse( { 'status':'error' })


def ajax_report_comment(request):
	class SendMailThread(threading.Thread):
		def run(self):
			plain_text = comment.name+u' 在粉絲專頁的留言被多個人檢舉，請確認該留言是否適當\n留言內容 ： '+ comment.message+u'\nFacebook 貼文 : '+comment.facebook_post_url +u'\n清大攝影競賽資料庫 ： '+settings.DOMAIN_NAME + reverse('admin:photos_reportedcomment_changelist')
			html_str = render_to_string('photos/report_comment_email_template.html', { 'comment': comment, 'domain_name': settings.DOMAIN_NAME } )
			mail_admins('Facebook reported commands', plain_text , html_message=html_str)


	if ( request.method == 'POST' and 'facebook_post_id' in request.POST and 'facebook_comment_id' in request.POST and 'user_id' in request.POST and 'name' in request.POST and 'message' in request.POST):
		'''
		if 'report_comment_list' in request.session:
			request.session['report_comment_list'] += [ request.POST['facebook_comment_id'] ]
		else:
			request.session['report_comment_list'] = [ request.POST['facebook_comment_id'] ]
		'''

		try:
			comment = ReportedComment.objects.get(facebook_comment_id=request.POST['facebook_comment_id'])
			delta =  timezone.now() - comment.last_report_time
			if delta.days <= 3:
				if request.POST['user_id'] not in comment.report_list:
					comment.report_count += 1
					comment.report_list += ','+request.POST['user_id']

					if comment.report_count >= 5 :
						SendMailThread().start()
			else:
				comment.report_count = 1
				comment.report_list = request.POST['user_id']

			comment.last_report_time = timezone.now()
			comment.save(update_fields=['report_count', 'report_list','last_report_time'])
			return JsonResponse({'status':'ok'})

		except ObjectDoesNotExist as  e:
			tmp_list = request.POST['facebook_post_id'].split('_')
			if len(tmp_list) == 2:
				post_url = 'https://www.facebook.com/{}/posts/{}'.format(*tmp_list)
				comment = ReportedComment.objects.create(facebook_post_url=post_url, facebook_comment_id = request.POST['facebook_comment_id'], name=request.POST['name'], message=request.POST['message'], report_count=1, report_list=request.POST['user_id'] )
				return JsonResponse({'status':'ok'})
			else:
				return JsonResponse({'status': 'error'})
		except Exception as e :
			return JsonResponse({'status': 'error'})
	else:
		return JsonResponse({'status': 'error'})

