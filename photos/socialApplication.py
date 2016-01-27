#-*- encoding=UTF-8 -*-
import flickr_api
import facebook
import json
import time
import threading
from django.utils import timezone
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from .authorization_token import __facebook_page_token, __flickr_api_key, __flickr_api_secret
from .models import Photo,Tag

def run_in_thread(func):
	'''
		used for decorator
	'''
	def thread_func(*args, **kwargs):
		threading.Thread(target=func, args=args, kwargs=kwargs).start()
	return thread_func

class Comment(object):
	'''
		制定一個Comment需要有的資料，toDitc可以把object轉換成一個dictionary用於serial傳送
		self.user_name = 回覆者的名稱
		self.user_photo_url = 回覆者的大頭貼
		self.comment_text = 回覆的內容
		self.comment_facebook_id = 這篇回覆的facebok_id;
	'''
	def __init__(self, user_name, user_photo_url, comment_text, comment_facebook_id):
		super(Comment, self).__init__()
		self.user_name = user_name;
		self.user_photo_url = user_photo_url;
		self.comment_text = comment_text;
		self.comment_facebook_id = comment_facebook_id;

	def toDict(self):
		return {
			'user_name':self.user_name,
			'user_photo_url':self.user_photo_url,
			'comment_text': self.comment_text,
			'comment_facebook_id': self.comment_facebook_id,
		}

def uploadPhoto(photo):
	'''
		先將照片上傳到 Flickr，再張貼到 Facebook。
		Flickr驗證會用到 oauth_verifier.txt ，要放在 NTHUFC 根目錄中
		authorization_token.py 存放 Facebook 和 Flickr 驗證會用到的資訊，不要放到 github 上
	'''

	if not photo.isReady:
		for tag_text in photo.tags.split(' '):
			if tag_text == '':
				continue
			try:
				tag = Tag.objects.get(tag_name = tag_text)
				tag.update_time = timezone.now()
				tag.tag_count += 1
				tag.save()
			except ObjectDoesNotExist:
				Tag.objects.create(tag_name=tag_text)

		uploadUsingThread(photo)



def getFacebookPostContent(photo, isValid=True, photo_info={}):
	'''
		產生Facebook的貼文內容，會在標籤地點跟拍攝者前面加上'#'形成facebook的tag
	'''


	if isValid:
		label = ' '+photo.tags;
		label = label.replace(' ',' #');
		return u'{} {}\n===================\n地點: #{}\n拍攝者: #{}\n\n{}\n \n活動網站：http://photos.cc.nthu.edu.tw/\nFlickr照片連結: https://www.flickr.com/photos/138506275@N05/{}'.format(
			photo.title, label, photo.location_marker.title, photo.owner.nickname, photo.content, photo.flickr_photo_id)
	else:
		label = ' '+photo_info['tags'];
		label = label.replace(' ',' #');
		return u'[無效]{} {} \n===================\n地點: #{}\n[這張照片已經被投稿者移除，它的票數不會列入計分]\n\n{}\n \n活動網站：http://photos.cc.nthu.edu.tw/\nFlickr照片連結: https://www.flickr.com/photos/138506275@N05/{}'.format(
			photo_info['title'], label, photo_info['location_marker_title'], photo_info['content'], photo_info['flickr_photo_id'])

@run_in_thread
def uploadUsingThread(photo):
	photo_file_path = photo.image.path
	result = {}

	if photo.flickr_photo_id=='':
		try_count = 3
		flickr_api.set_keys(api_key = __flickr_api_key, api_secret = __flickr_api_secret)
		flickr_api.set_auth_handler('oauth_verifier.txt')

		while try_count > 0 :
			try :
				flickr_response = flickr_api.upload(
					photo_file = photo_file_path,
					title =photo.title,
					description = u'地點: '+photo.location_marker.title+u'\n拍攝者: '+photo.owner.nickname+'\n\n'+photo.content,
					tags = photo.tags,
					is_public = 1,
					is_family = 1,
					is_friend = 1,
					safety_level =1,
					content_type  =1,
					hidden = 1,
				)
				photo.flickr_photo_id = flickr_response.id
				photo_info = flickr_response.getInfo()
				photo.flickr_photo_url = 'https://farm{}.staticflickr.com/{}/{}_{}.jpg'.format(photo_info['farm'], photo_info['server'], flickr_response.id, photo_info['secret'])
				photo.save()
				result['flickr_response'] = flickr_response
				break;
			except Exception as e:
				print str(e)
				try_count -= 1
			time.sleep(10)
	else:
		result['flickr_response'] = 'already upload to flickr'

	if photo.facebook_post_id =='':
		result['facebook_response'] = uploadToFacebook(photo)
	else:
		result['facebook_response'] = updateFlickrPhotoURL(photo)

	print 'uploadPhotoresult' + str(result)

	photo.isReady = True
	photo.image.delete()
	photo.save()
	return result

def uploadToFacebook(photo):
	'''
		將新的照片張貼到Facebook，並把貼文ID存起來
	'''
	graph = facebook.GraphAPI(access_token=__facebook_page_token, version='2.5')

	photo_file_path = photo.image.path
	facebook_response = graph.put_photo(
		image= open(photo_file_path,'rb'),
		message= getFacebookPostContent(photo)
	)
	photo.facebook_post_id = facebook_response['post_id']
	photo.save()
	return facebook_response

def updateFlickrPhotoURL(photo):
	'''
		如果該篇照片已經有Facebook貼文的ID，那就更新貼文內容而不要重新張貼
	'''
	graph = facebook.GraphAPI(access_token=__facebook_page_token, version='2.5')

	facebook_response = graph.update_photo(
		facebook_post_id=photo.facebook_post_id,
		message= getFacebookPostContent(photo)
	)
	return facebook_response

def getPhotoDetails(photo, user_access_token):
	'''
		取得某張照片的facebook讚數、評論跟內容，和flickr的收藏數
		如果使用者有登入的話，確認使用者是否有按過讚了
	'''
	__facebook_query_field = 'likes.summary(true), comments{from{name, picture{url}}, message}'
	graph = facebook.GraphAPI(access_token=__facebook_page_token, version='2.5')
	response = graph.get_object(id=photo.facebook_post_id, fields=__facebook_query_field)
	comment_list = []

	if 'comments' in response:
		for item in response['comments']['data']:
			comment_list.append(
				Comment(
					user_name=item['from']['name'],
					user_photo_url=item['from']['picture']['data']['url'],
					comment_text=item['message'],
					comment_facebook_id=item['id'],
				)
			)
	facebook_likes = response['likes']['summary']['total_count']

	flickr_api.set_keys(api_key = __flickr_api_key, api_secret = __flickr_api_secret)
	flickr_api.set_auth_handler('oauth_verifier.txt')
	favorites = flickr_api.Photo(id = photo.flickr_photo_id).getFavorites()

	return {
		'facebook_likes': facebook_likes,
		'facebook_post_id': photo.facebook_post_id,
		'comment_list': [ x.toDict() for x in comment_list],
		'flickr_favorites': len(favorites),
		'photo_url': photo.flickr_photo_url,
		'photo_content': getFacebookPostContent(photo),
		'user_has_like': getHasLiked(photo.facebook_post_id,user_access_token),
	}

def postComment(access_token, photo_facebook_id, comment_text):
	'''
		張貼新的comment到facebook上，回傳新的comment清單
	'''
	try:
		graph = facebook.GraphAPI(access_token=access_token, version='2.5')
		response = graph.put_comment(object_id=photo_facebook_id, message=comment_text)
	except Exception, e:
		print(e)

	graph = facebook.GraphAPI(access_token=__facebook_page_token, version='2.5')
	response = graph.get_object(id=photo_facebook_id, fields='comments{from{name, picture{url}}, message}')
	comment_list = []
	if 'comments' in response:
		for item in response['comments']['data']:
			comment_list.append(
				Comment(
					user_name=item['from']['name'],
					user_photo_url=item['from']['picture']['data']['url'],
					comment_text=item['message'],
					comment_facebook_id=item['id'],
				)
			)
	return [ x.toDict() for x in comment_list]

def postLike(user_access_token, photo_facebook_id):
	'''
		按某張造片的讚，並回傳照片的總讚數
	'''
	try:
		graph = facebook.GraphAPI(access_token=user_access_token, version='2.5')
		response = graph.put_like(object_id=photo_facebook_id)
	except Exception, e:
		print str(e)

	graph = facebook.GraphAPI(access_token=__facebook_page_token, version='2.5')
	response = graph.get_object(id=photo_facebook_id, fields='likes.summary(true)')
	return response['likes']['summary']['total_count']

def getHasLiked(photo_facebook_id, user_access_token):
	'''
		確認使用者是否按過某篇照片的讚
	'''

	try:
		graph = facebook.GraphAPI(access_token=user_access_token, version='2.5')
		response = graph.get_object(id=photo_facebook_id, fields='likes.summary(true)')
		if (not 'error' in response) and 'likes' in response:
			return response['likes']['summary']['has_liked']
		else:
			return False
	except Exception, e:
		print str(e)
		return False

@run_in_thread
def deletePhoto(photo_info):
	result = {}
	graph = facebook.GraphAPI(access_token=__facebook_page_token, version='2.5')
	facebook_response = graph.update_photo(
		facebook_post_id=photo_info['facebook_post_id'],
		message= getFacebookPostContent(None, isValid=False, photo_info=photo_info)
	)

	flickr_api.set_keys(api_key = __flickr_api_key, api_secret = __flickr_api_secret)
	flickr_api.set_auth_handler('oauth_verifier.txt')
	uni_title = u'[無效] '+ photo_info['title']
	uni_title = uni_title.encode('utf-8')
	uni_description = u'[這張照片已經被投稿者移除，它的票數不會列入計分]\n\n'+ photo_info['content']
	uni_description = uni_description.encode('utf-8')

	flick_response = flickr_api.objects.Photo(
        id=photo_info['flickr_photo_id'],
        editurl='https://www.flickr.com/photos/upload/edit/?ids=' + photo_info['flickr_photo_id']
    ).setMeta(
    	title=uni_title,
		description=uni_description,
	)

	result['facebook_response'] = facebook_response
	result['flick_response'] = flick_response
	#photo.image.delete()
	print 'deletePhoto result:'+str(result)
	return result

def getVotes(photo):
	flickr_api.set_keys(api_key = __flickr_api_key, api_secret = __flickr_api_secret)
	flickr_api.set_auth_handler('oauth_verifier.txt')
	favorites = flickr_api.Photo(id = photo.flickr_photo_id).getFavorites()

	graph = facebook.GraphAPI(access_token=__facebook_page_token, version='2.5')
	response = graph.get_object(id=photo.facebook_post_id, fields='likes.summary(true)')
	likes =  response['likes']['summary']['total_count']
	photo.favorites = len(favorites)
	photo.likes = likes
	photo.votes = photo.likes + photo.favorites
	photo.last_modified_time = timezone.now()
	photo.save(update_fields=['favorites','likes','votes','last_modified_time'])
	return photo.favorites+photo.likes

def getCommentList(facebook_post_id):

	graph = facebook.GraphAPI(access_token=__facebook_page_token, version='2.5')
	res = graph.get_object(id=facebook_post_id, fields='comments')
	if res.has_key('comments'):
		response = graph.get_object(id=facebook_post_id, fields='comments{likes.summary(total_count),from{name, picture{url}}, message}')

	else:
		return []


	comment_list = []
	for c in response['comments']['data']:
		comment_list.append({
			'comment_id': c['id'],
			'message': c['message'],
			'name': c['from']['name'],
			'avatar_url': c['from']['picture']['data']['url'],
			'likes_count': c['likes']['summary']['total_count'],
		})

	return comment_list

def getPhotoModalDetails(photo):

	obj = {
		'title': photo.title,
		'votes': photo.votes,
		'content': photo.content,
		'comment_list': getCommentList(photo.facebook_post_id),
		'location': photo.location_marker.title,
		'tags': photo.tags,
		'owner': photo.owner.nickname,
		'photo_url': photo.flickr_photo_url,
		'flickr_url': 'https://www.flickr.com/photos/138506275@N05/'+photo.flickr_photo_id,
		'facebook_post_id': photo.facebook_post_id,
	}
	#print obj
	return obj

def addFlickrFavorite(request_token_key, request_token_secret,oauth_verifier,photo_id):
	flickr_api.set_keys(api_key = __flickr_api_key, api_secret = __flickr_api_secret)
	a = flickr_api.auth.AuthHandler(request_token_key=request_token_key , request_token_secret=request_token_secret)
	a.set_verifier(oauth_verifier)
	flickr_api.set_auth_handler(a)
	photo = flickr_api.Photo(id=photo_id)
	photo.addToFavorites();
	dd = a.todict()
	return (dd['access_token_key'],dd['access_token_secret'])

def getFlickrAuthorizationUrl(photo_id):
	__DOMAIN_NAME = 'http://www.localhost:8000'
	flickr_api.set_keys(api_key = __flickr_api_key, api_secret = __flickr_api_secret)
	a = flickr_api.auth.AuthHandler(callback=__DOMAIN_NAME+reverse('photos:flickr_authorization_redirect', args=(photo_id,)))
	#a = flickr_api.auth.AuthHandler()
	dd = a.todict()
	return (a.get_authorization_url('write'), dd['request_token_key'],dd['request_token_secret'])
