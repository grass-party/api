from rest_framework import status
from rest_framework import response
from rest_framework import viewsets

from commons import blockchain
from agenda import models
from agenda import serializers


class AgendaViewSet(viewsets.ModelViewSet):
    queryset = models.Agenda.objects.all()
    serializer_class = serializers.AgendaSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        agenda = serializer.save()

        blockchain.Set.agenda(agenda)

        return response.Response(
            status=status.HTTP_201_CREATED,
            headers=self.get_success_headers(serializer.data)
        )
