import json

from django import test


class TestClient(test.Client):
    def post(self, *args, **kwargs):
        data = kwargs.get('data')
        if data:
            kwargs['data'] = json.dumps(data)
            kwargs['content_type'] = 'application/json'

        return super().post(*args, **kwargs)


class TestCase(test.TestCase):
    client_class = TestClient

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = test.Client()
