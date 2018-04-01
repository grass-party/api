from django.contrib.auth import get_user_model
from django.db import IntegrityError

from rest_framework import decorators
from rest_framework import response
from rest_framework import status
from rest_framework import serializers
from rest_framework import views
from rest_framework import viewsets

from commons import blockchain
from user import oauth
from user.serializers import UserSerializer
from user.models import SocialAccount


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    @decorators.list_route(methods=['post'], url_path='register_pubkey')
    def pubkey(self, request):
        pubkey = request.data.get('account_pubkey')
        if not pubkey:
            raise serializers.ValidationError({
                'account_pubkey': ['account_pubkey field is required'],
            })

        blockchain.Set.pubkey(1, pubkey)

        return response.Response(status=status.HTTP_201_CREATED)

    @decorators.list_route(methods=['get'], url_path='sessions')
    def check_sessions(self, request):
        user = get_user_model().objects.all()[0]  # for test
        data = UserSerializer(user).data
        return response.Response(data, status=status.HTTP_200_OK)


@decorators.api_view(['GET'])
def callback_oauth_user_create(request):
    code = request.data.get('code')
    state = request.data.get('state')
    if not code or not state:
        errors = {}
        if not code:
            errors['code'] = ['code field is required']
        if not state:
            errors['state'] = ['state field is required']
        raise serializers.ValidationError(errors)

    token_result = oauth.Naver.get_token(code, state)
    profile_result = oauth.Naver.get_profile(token_result['access_token'])

    try:
        user = get_user_model().objects\
            .create_user(email=profile_result['email'], password='social')
    except IntegrityError:
        raise serializers.ValidationError('email already exists')

    social_account_params = {
        'user_id': user.id,
        'provider': 'naver',
        'account_id': profile_result['id'],
        'email': profile_result['email'],
    }
    SocialAccount.objects.create(**social_account_params)

    user.social_auth(request, token_result['access_token'],
                     token_result['refresh_token'], token_result['expires_in'])

    return response.Response(status.HTTP_200_OK)


@decorators.api_view(['GET'])
def callback_oauth_session_create(request):
    code = request.data.get('code')
    state = request.data.get('state')
    if not code or not state:
        errors = {}
        if not code:
            errors['code'] = ['code field is required']
        if not state:
            errors['state'] = ['state field is required']
        raise serializers.ValidationError(errors)

    token_result = oauth.Naver.get_token(code, state)
    profile_result = oauth.Naver.get_profile(token_result['access_token'])

    user = get_user_model().objects\
        .filter(email=profile_result['email']).first()
    user.social_auth(request, token_result['access_token'],
                     token_result['refresh_token'], token_result['expires_in'])

    return response.Response(status.HTTP_200_OK)
