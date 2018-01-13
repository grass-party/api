from rest_framework import serializers

from .models import Agenda
from user.serializers import UserSerializer


class AgendaSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Agenda
        fields = ('owner', 'title', 'description', 'created_at', 'updated_at',)
