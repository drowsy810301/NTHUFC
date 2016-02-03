# -*- coding:utf-8 -*-

from authorization_token import __flickr_api_key, __flickr_api_secret, fb_fanpage_graph
import flickr_api
import facebook

print 'Testing Flickr API ...'
flickr_api.set_keys(api_key = __flickr_api_key, api_secret = __flickr_api_secret)
a = flickr_api.auth.AuthHandler()
url = a.get_authorization_url('delete')
print url
verifier_code = raw_input('verifier code = ')
a.set_verifier(verifier_code)
a.save('oauth_verifier.txt')
flickr_api.set_auth_handler('oauth_verifier.txt')

user = flickr_api.test.login()
print user

print 'Testing Facebook API...'
page = fb_fanpage_graph.get_object(id='1528712347441804')
print '{} (id = {})'.format(page['name'].encode('utf-8'), page['id'])
