from rest_framework import decorators
from rest_framework import response
from rest_framework import status
from rest_framework import serializers
from rest_framework import viewsets

from commons import blockchain
from agenda.models import Agenda
from agenda.serializers import AgendaSerializer


class AgendaViewSet(viewsets.ModelViewSet):
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer

    @decorators.list_route(methods=['post'], url_path='blockchain')
    def create_blockchain(self, request):
        agenda_id = request.data.get('agenda_id')
        if not agenda_id:
            raise serializers.ValidationError({
                'agenda_id': ['agenda_id field is required'],
            })

        agenda = Agenda.objects.get(agenda_id)
        blockchain.Set.agenda(agenda)

        return response.Response(
            status=status.HTTP_201_CREATED,
        )

    @decorators.detail_route(methods=['post'], url_path='vote')
    def vote(self, request, id=None):
        vote = request.data.get('vote')
        if not vote:
            raise serializers.ValidationError({
                'vote': ['vote field is required'],
            })

        blockchain.Set.vote(1, id, vote)

        return response.Response(
            status=status.HTTP_201_CREATED,
        )
