from unittest import mock

from django.contrib.auth import get_user_model

from commons import tests


class TestNaverUserCreate(tests.TestCase):
    @mock.patch('user.oauth.Naver.get_token')
    def test_success(self, naver_get_token):
        naver_get_token.return_value = {
            'access_token': '',
            'refresh_token': '',
            'expires_in': 60 * 60,
        }

        before_create_count = get_user_model().objects.count()

        params = {

        }
        resp = self.client.post('/users/create_naver/', params)
        self.assertEqual(resp.status_code, 201)

        after_create_count = get_user_model().objects.count()
        self.assertEqual(before_create_count + 1, after_create_count)
        new_user = get_user_model().objects\
            .order_by('-date_joined')\
            .all()[0]
        self.assertEqual(new_user.social, 'naver')


class TestUserRegisterPubkey(tests.TestCase):
    @mock.patch('commons.blockchain.Set.pubkey')
    def test_success(self, set_publkey):
        set_publkey.return_value = {}

        resp = self.client.post('/users/register_pubkey/', {
            'pubkey': 'my public key',
        })

        self.assertEqual(resp.status_code, 201)

    @mock.patch('commons.blockchain.Set.pubkey')
    def test_no_pubkey_param(self, set_publkey):
        set_publkey.return_value = {}

        resp = self.client.post('/users/register_pubkey/', {
            'no pubkey': 'this is not a public key',
        })

        self.assertEqual(resp.status_code, 400)


class TestCreateSession(tests.TestCase):
    def test_success(self):
        pass


class TestDeleteSession(tests.TestCase):
    def test_success(self):
        pass
