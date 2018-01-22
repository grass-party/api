import hashlib

from django.contrib.auth import get_user_model
from django.db import models


class Agenda(models.Model):
    owner = models.ForeignKey(get_user_model(), related_name='agendas',
                              on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    is_publish = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def blockchain_serialize(self):
        agenda_created_at = self.created_at.strftime('%Y%m%d')
        target_data = f'[id:{self.id}]'
        target_data += f'[title:{self.title}]'
        target_data += f'[description:{self.description}]'
        target_data += f'[created_at:{agenda_created_at}]'

        choices = self.choices.order_by('order').all()
        for choice in choices:
            target_data += f'[choice_order:{choice.order}]'
            target_data += f'[choice_title:{choice.title}]'

        target_data = hashlib.sha512(target_data.encode()).hexdigest()
        return target_data


class Choice(models.Model):
    agenda = models.ForeignKey('Agenda', related_name='choices',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    order = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Tag(models.Model):
    agendas = models.ManyToManyField('Agenda')
    title = models.CharField(max_length=30, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
