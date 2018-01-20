from rest_framework import status
from rest_framework import response
from rest_framework import viewsets

from commons import blockchain
from agenda.models import Agenda
from agenda.serializers import AgendaSerializer


class AgendaViewSet(viewsets.ModelViewSet):
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        agenda = serializer.save()
        blockchain.Set.agenda(agenda)

        return response.Response(
            status=status.HTTP_201_CREATED,
            headers=self.get_success_headers(serializer.data)
        )
