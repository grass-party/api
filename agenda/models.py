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


class Choice(models.Model):
    agenda = models.ForeignKey('Agenda', related_name='choices',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True)
    order = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Tag(models.Model):
    agendas = models.ManyToManyField('Agenda')
    title = models.CharField(max_length=30, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
