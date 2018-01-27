from unittest import mock

from django.contrib.auth import get_user_model

from commons import tests
from agenda.models import Agenda
from agenda.serializers import AgendaSerializer


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

    def test_no_agenda_params(self):
        params = {}
        resp = self.client.post('/agendas/', data=params)

        self.assertEqual(resp.status_code, 400)
        self.assertIn('title', resp.data)
        self.assertIn('description', resp.data)
        self.assertIn('choices', resp.data)

    def test_no_choices_params(self):
        params = {
            'title': 'my title',
            'description': 'my description',
            'choices': [{
                'not title': 'not title', 'not order': 'not order',
            }],
        }
        resp = self.client.post('/agendas/', data=params)

        self.assertEqual(resp.status_code, 400)
        self.assertIn('choices', resp.data)
        self.assertIn('title', resp.data['choices'][0])
        self.assertIn('order', resp.data['choices'][0])


class TestAgendaCreateBlockChain(tests.TestCase):
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
        serializer = AgendaSerializer(data=params)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        cls.current_agenda = Agenda.objects.filter(title='my title').first()

    @mock.patch('commons.blockchain.Set.agenda')
    def test_success(self, set_agenda):
        set_agenda.return_value = {}

        params = {
            'agenda_id': self.current_agenda.id,
        }
        resp = self.client.post('/agendas/blockchain/', data=params)

        self.assertEqual(resp.status_code, 201)

    @mock.patch('commons.blockchain.Set.agenda')
    def test_no_agenda_id(self, set_agenda):
        set_agenda.return_value = {}

        params = {}
        resp = self.client.post('/agendas/blockchain/', data=params)

        self.assertEqual(resp.status_code, 400)
        self.assertIn('agenda_id', resp.data)


class TestAgendaCreateVote(tests.TestCase):
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
        serializer = AgendaSerializer(data=params)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        cls.current_agenda = Agenda.objects.filter(title='my title').first()

    @mock.patch('commons.blockchain.Set.vote')
    def test_success(self, set_agenda):
        set_agenda.return_value = {}

        params = {
            'vote': 1,
        }
        resp = self.client.post(f'/agendas/{self.current_agenda.id}/vote/',
                                data=params)

        self.assertEqual(resp.status_code, 201)

    @mock.patch('commons.blockchain.Set.vote')
    def test_no_vote(self, set_agenda):
        set_agenda.return_value = {}

        params = {}
        resp = self.client.post(f'/agendas/{self.current_agenda.id}/vote/',
                                data=params)

        self.assertEqual(resp.status_code, 400)
        self.assertIn('vote', resp.data)

    @mock.patch('commons.blockchain.Set.vote')
    def test_wrong_vote(self, set_agenda):
        set_agenda.return_value = {}

        params = {
            'vote': 3,
        }
        resp = self.client.post(f'/agendas/{self.current_agenda.id}/vote/',
                                data=params)

        self.assertEqual(resp.status_code, 400)
        self.assertIn('vote', resp.data)
