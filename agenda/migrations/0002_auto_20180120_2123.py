# Generated by Django 2.0 on 2018-01-20 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='agenda',
            name='is_publish',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='agenda',
            name='published_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
