from unittest import mock

from commons import tests


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
