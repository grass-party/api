from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'context' in kwargs and 'request' in kwargs['context']:
            request = kwargs['context']['request']
            # dynamic serializer fields
            if 'register_pubkey' in request.path:
                self.fields['pubkey'] = serializers.CharField(max_length=8000)
                del self.fields['email']

    class Meta:
        model = get_user_model()
        fields = ('email',)
