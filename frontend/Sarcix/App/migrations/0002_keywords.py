# Generated by Django 2.2.7 on 2019-11-08 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Keywords',
            fields=[
                ('event_id', models.CharField(max_length=6, primary_key=True, serialize=False)),
                ('event_title', models.TextField()),
                ('term', models.TextField()),
                ('desc_uid', models.CharField(max_length=10)),
                ('con_uid', models.CharField(max_length=10)),
                ('score', models.IntegerField()),
            ],
            options={
                'db_table': 'keywords1',
                'managed': True,
                'unique_together': {('event_id', 'event_title')},
            },
        ),
    ]
