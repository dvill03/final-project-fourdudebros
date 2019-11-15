# Generated by Django 2.2.7 on 2019-11-08 00:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Run',
            fields=[
                ('event_name', models.TextField(primary_key=True, serialize=False)),
                ('coverage_name', models.TextField()),
                ('score', models.DecimalField(decimal_places=2, max_digits=3, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)])),
            ],
            options={
                'db_table': 'run1',
                'managed': True,
                'unique_together': {('event_name', 'coverage_name')},
            },
        ),
    ]
