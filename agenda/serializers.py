from rest_framework import serializers

from user.serializers import UserSerializer
from agenda.models import Agenda, Choice


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = (
            'title', 'order',
        )


class AgendaSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Agenda
        fields = (
            'id', 'title', 'description',
            'is_publish', 'published_at', 'created_at', 'updated_at',
            'owner', 'choices',
        )
        read_only_fields = (
            'id',
            'is_publish', 'published_at', 'created_at', 'updated_at',
            'owner',
        )

    def validate_choices(self, choices):
        if not choices:
            raise serializers.ValidationError('choices field is required')
        return choices

    def create(self, validated_data):
        choices_data = validated_data.pop('choices')

        # request = self.context['request']
        # validated_data['owner_id'] = request.user.id
        validated_data['owner_id'] = 1  # test

        agenda = Agenda.objects.create(**validated_data)
        for choice_data in choices_data:
            choice_data['agenda_id'] = agenda.id
            Choice.objects.create(**choice_data)

        return agenda
