import json
import hashlib

from django.conf import settings
import requests


class Set:
    root = f'{settings.BLOCKCHAIN_HOST}'

    @classmethod
    def pubkey(cls, user_id, pubkey):
        url = f'{cls.root}/register'
        data = json.dumps({
            'id': str(user_id),
            'pubkey': pubkey,
        })
        headers = {
            'Content-Type': 'application/json',
        }
        resp = requests.post(url, data=data, headers=headers)

        return resp

    @classmethod
    def agenda(cls, agenda):
        agenda_created_at = agenda.created_at.strftime('%Y%m%d')
        target_data = f'{agenda.id}{agenda.title}{agenda.description}\
            {agenda_created_at}'
        for choice in agenda.choices:
            choice_created_at = agenda.created_at.strftime('%Y%m%d')
            target_data += f'{choice.title}{choice_created_at}'
        target_data = hashlib.sha512(target_data).hexdigest()

        url = f'{cls.root}/asdf'
        resp = requests.post(url, data=json.dumps({
            'id': agenda.id,
            'data': target_data,
        }))

        return resp


class Get:
    root = f'{settings.BLOCKCHAIN_HOST}'
