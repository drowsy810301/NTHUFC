from photos.authorization_token import __facebook_page_token, __flickr_api_key, __flickr_api_secret
import flickr_api

flickr_api.set_keys(api_key = __flickr_api_key, api_secret = __flickr_api_secret)

a = flickr_api.auth.AuthHandler(callback = "http://photos.cc.nthu.edu.tw/")
url = a.get_authorization_url('write')
print url
code = input('verifier code = ');
a.set_verifier(code)
flickr_api.set_auth_handler(a)


