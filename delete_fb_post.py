from photos.authorization_token import __facebook_page_token, __flickr_api_key, __flickr_api_secret
import facebook

graph = facebook.GraphAPI(access_token=__facebook_page_token, version='2.5')

while True:
	photos = graph.get_connections(id='me', connection_name='feed')
	if not photos['data']:
		break

	for p in photos['data']:
		graph.delete_object(id=p['id'])

