# NTHUFC

####Dependencies:
* python2.7
* python-dev
* mysql-server
* python-pip
* python-mysqldb
* django-crispy-forms
* django-axes
* pillow
* [django-bower](http://django-bower.readthedocs.org/en/latest/installation.html)
* [facebook-sdk](https://github.com/pythonforfacebook/facebook-sdk)
* [python_oauth](https://github.com/joestump/python-oauth2)
* [python-flickr-api](https://github.com/alexis-mignon/python-flickr-api)

####Authorization Files:
* put **oauth_verifier.txt** in the project root directory

    File template: (there are only **2** line, **WITHOUT** quotes)

        'access_token_key'
        'access_token_secret'

* put **authorization_token.py** in photos/

    File template:

        import facebook
        __facebook_page_token = 'XXX'
        __flickr_api_key = 'YYY'
        __flickr_api_secret = 'ZZZ'

        fb_fanpage_graph = facebook.GraphAPI(access_token=__facebook_page_token, version='2.5')
