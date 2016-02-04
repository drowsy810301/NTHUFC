# -*- coding:utf-8 -*-

from authorization_token import __flickr_api_key, __flickr_api_secret, __facebook_page_token
import flickr_api
import facebook

print 'Testing Flickr API ...'
flickr_api.set_keys(api_key = __flickr_api_key, api_secret = __flickr_api_secret)
a = flickr_api.auth.AuthHandler()
url = a.get_authorization_url('delete')
print url
verifier_code = raw_input('verifier code = ')
try:
	a.set_verifier(verifier_code)
	a.save('oauth_verifier.txt')
	flickr_api.set_auth_handler('oauth_verifier.txt')

	user = flickr_api.test.login()
	print user
except Exception as e:
	print str(e)

print 'Testing Facebook API...'
graph = facebook.GraphAPI(access_token= __facebook_page_token, version='2.5')
page = graph.get_object(id='492779200909805')
print '{} (id = {})'.format(page['name'].encode('utf-8'), page['id'])
