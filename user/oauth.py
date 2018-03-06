from django.conf import settings
from rest_framework import exceptions

import requests


class Naver:
    naver = settings.OPEN_API['naver']

    @classmethod
    def get_token(cls, code, state):
        params = {
            'client_id': cls.naver['client_id'],
            'client_secret': cls.naver['client_secret'],
            'grant_type': 'authorization_code',
            'code': code,
            'state': state,
        }
        host = cls.naver['oauth_host']
        resp = requests.post(f'{host}/oauth2/token', data=params)

        error_code = resp.data.get('error')
        error_description = resp.data.get('error_description')
        if error_code or error_description:
            raise exceptions.AuthenticationFailed(
                'fail to get naver token with error: ' +
                f'{error_code} {error_description}')

        return resp.data

    @classmethod
    def get_profile(cls, token):
        headers = {
            'Authorization': f'Bearer {token}',
        }
        host = cls.naver['host']
        resp = requests.post(f'{host}/v1/nid/me', headers=headers)

        account_id = resp.data['response'].get('id')
        email = resp.data['response'].get('email')
        if not account_id or not email:
            status_code = resp.data['resultcode']
            message = resp.data['message']
            raise exceptions.APIException(
                'fail to get naver profile with error: ' +
                f'{status_code} {message}')

        return resp.data['response']
