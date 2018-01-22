import json

from django.conf import settings
import requests


class Set:
    root = f'{settings.BLOCKCHAIN_HOST}'

    @classmethod
    def _req(cls, path, data):
        url = f'{cls.root}/{path}'
        data = json.dumps(data)
        headers = {
            'Content-Type': 'application/json',
        }
        resp = requests.post(url, data=data, headers=headers)
        return resp

    @classmethod
    def pubkey(cls, user_id, pubkey):
        resp = cls._req('register', {
            'id': str(user_id),
            'pubkey': pubkey,
        })
        return resp

    @classmethod
    def agenda(cls, agenda):
        resp = cls._req('setAgenda', {
            'id': agenda.id,
            'data': agenda.blockchain_serialize(),
        })
        return resp

    @classmethod
    def vote(cls, user_id, agenda_id, vote):
        resp = cls._req('vote', {
            'id': f'{user_id}-{agenda_id}',
            'data': vote,
        })
        return resp


class Get:
    root = f'{settings.BLOCKCHAIN_HOST}'
