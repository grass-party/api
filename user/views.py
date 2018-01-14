from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework import decorators
from rest_framework import response
from rest_framework import status

from commons import blockchain
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    @decorators.list_route(methods=['post'], url_path='register_pubkey')
    def register_pubkey(self, request):
        pubkey = request.data.get('pubkey')

        # blockchain.Set.pubkey(request.user.id, pubkey)
        blockchain.Set.pubkey(1, pubkey)  # test

        return response.Response(
            status=status.HTTP_201_CREATED,
        )
