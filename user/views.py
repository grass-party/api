from django.contrib.auth import get_user_model
from rest_framework import decorators
from rest_framework import response
from rest_framework import status
from rest_framework import serializers
from rest_framework import viewsets

from commons import blockchain
from user.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    @decorators.list_route(methods=['post'], url_path='register_pubkey')
    def register_pubkey(self, request):
        pubkey = request.data.get('pubkey')
        if not pubkey:
            raise serializers.ValidationError({
                'pubkey': ['pubkey field is required'],
            })

        blockchain.Set.pubkey(1, pubkey)

        return response.Response(
            status=status.HTTP_201_CREATED,
        )
