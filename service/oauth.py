from typing import List, Dict

from flask import request, redirect, url_for
from urllib.request import urlopen
from rauth import OAuth2Service
import json

class OAuthSignIn(object):

    providers = None

    def __init__(self, provider_name):
        self.providers = None
        self.provider_name = provider_name
        credentials = {"id": "409979230610-d7095hu6nf30bmju8kek2610345pkruf.apps.googleusercontent.com",
                       "secret": "6e3cjzDfvmydKelJGDrByTVy"}
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']

    def authorize(self):
        pass

    def callback(self):
        pass

    def get_callback_url(self):
        return url_for('oauth.oauth_callback', provider=self.provider_name,
                        _external=True)

    @classmethod
    def get_provider(self, provider_name):
        if self.providers is None:
            self.providers={}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]


class GoogleSignIn(OAuthSignIn):
    def __init__(self):
        super(GoogleSignIn, self).__init__('google')
        googleinfo = urlopen('https://accounts.google.com/.well-known/openid-configuration')
        google_params = json.load(googleinfo)
        #google_params['scopes_supported'].append('userinfo.profile')
        self.service = OAuth2Service(
                name='google',
                client_id=self.consumer_id,
                client_secret=self.consumer_secret,
                authorize_url=google_params.get('authorization_endpoint'),
                base_url=google_params.get('userinfo_endpoint'),
                access_token_url=google_params.get('token_endpoint')
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope='https://www.googleapis.com/auth/userinfo.profile',
            response_type='code',
            redirect_uri=self.get_callback_url())
            )

    def callback(self):
        if 'code' not in request.args:
            return None, None, None
        oauth_session = self.service.get_auth_session(
                data={'code': request.args['code'],
                      'grant_type': 'authorization_code',
                      'redirect_uri': self.get_callback_url(),
                     },
                decoder = json.loads
        )
        me = oauth_session.get('').json()

        """
        response = self.service.get_raw_access_token(data={'code': request.args['code'],
                      'grant_type': 'authorization_code',
                      'redirect_uri': 'http://localhost/oauth/login',
                    'prompt': 'consent'
                     })
        """

        return (me['name'], 'email')
                #me['email'])