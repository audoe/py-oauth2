# -*- coding: utf-8 -*-

from libs.auth_code import AuthCode
from libs.access_token import AccessToken
from libs.request import Request
from libs.response import Response
from libs.connection import Connection

class Client(object):

    def __init__(self, client_id, client_secret, **opts):
        self.id = client_id
        self.secret = client_secret
        self.site = opts.pop('site', '')
        self.opts = { 'authorize_url': '/oauth/authorize',
                      'token_url': '/oauth/token',
                      'token_method': 'POST',
                      'connection_opts': {},
                      'raise_errors': True,
                    }
        self.opts.update(opts)

    def __repr__(self):
        return '<OAuth2 Client>'

    def authorize_url(self, params={}):
        return Connection.build_url(self.site, path=self.opts['authorize_url'], params=params)

    def token_url(self, params={}):
        return Connection.build_url(self.site, path=self.opts['token_url'], params=params)

    def request(self, method, url, **opts):
        options = { 'raise_errors': self.opts['raise_errors'],
                    'parse': opts.pop('parse', 'json'),
                  }
        url = Connection.build_url(self.site, path=url)
        response = Connection.run_request(method, url, **opts)
        response = Response(response, parse=options['parse'])

        status = response.status
        if status in (301, 302, 303, 307):
            # redirect
            return response
        elif status in range(200, 400):
            return response
        else:
            pass
        return response

    def get_token(self, **opts):
        response = self.request(self.opts['token_method'], self.token_url(), **opts)
        opts.update(response.parsed)
        return AccessToken.from_hash(self, **opts)

    @property
    def auth_code(self):
        return AuthCode(self)