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
            'account_id': str(user_id),
            'account_pubkey': pubkey,
        })
        return resp

    @classmethod
    def agenda(cls, agenda):
        resp = cls._req('setAgenda', {
            'agenda_id': str(agenda.id),
            'agenda_hash': agenda.blockchain_serialize(),
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

    @classmethod
    def _req(cls, path, data):
        url = f'{cls.root}/{path}'
        resp = requests.get(url, data=data)
        return resp

    @classmethod
    def symkey(cls, user_id):
        resp = cls._req('symkey', {
            'user_id': user_id,
        })
        return resp
