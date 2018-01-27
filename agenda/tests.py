from django.contrib.auth import get_user_model

from commons import tests


class TestAgendaCreate(tests.TestCase):
    @classmethod
    def setUpTestData(cls):
        # hard-coded user for test
        user_params = {
            'id': 1,
            'email': 'waitingforqodot@gmail',
            'password': 'password',
        }
        cls.current_user = get_user_model().objects\
            .create_superuser(**user_params)

    def test_success(self):
        params = {
            'title': 'my title',
            'description': 'my description',
            'choices': [{
                'title': 'my choice title',
                'order': 1,
            }, {
                'title': 'my choice title 2',
                'order': 2,
            }],
        }
        resp = self.client.post('/agendas/', data=params)

        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data['title'], params['title'])
        self.assertEqual(resp.data['description'], params['description'])
        self.assertEqual(resp.data['owner']['email'], self.current_user.email)
