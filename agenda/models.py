from django.contrib.auth import get_user_model
from django.db import models


class Agenda(models.Model):
    owner = models.ForeignKey(get_user_model(), related_name='agendas',
                              on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Choice(models.Model):
    agenda = models.ForeignKey('Agenda', related_name='choices',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Tag(models.Model):
    title = models.CharField(max_length=30)
    agendas = models.ManyToManyField('Agenda')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
