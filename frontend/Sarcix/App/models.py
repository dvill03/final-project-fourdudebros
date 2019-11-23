from django.db import models
from django import forms
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

# Temporary tables until we make more progress, index is made only using primary keys
# Currently running script from shell to load data to the DBtable, may be dealt as Command, from BaseCommand later on

#Also, later on forms will be used instead, this way we can pass all the data from the html files to the models
class Run(models.Model):
    event_name = models.TextField(primary_key=True)
    coverage_name = models.TextField()
    score = models.DecimalField(max_digits=3, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(1)])

    class Meta:
        managed = True
        db_table = 'run1'
        unique_together = (('event_name', 'coverage_name'),)

    def __str__(self):
        return 'run1'


class Test(models.Model):
    run_name = models.CharField(primary_key=True, max_length=50)
    event_names = ArrayField(base_field=models.TextField())
    coverage_names = ArrayField(base_field=models.TextField())
    scores = ArrayField(models.DecimalField(max_digits=3, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(1)]))


class Keywords(models.Model):
    event_id = models.CharField(primary_key=True, max_length=6)
    event_title = models.TextField()
    term = models.TextField()
    desc_uid = models.CharField(max_length=10)
    con_uid = models.CharField(max_length=10)
    score = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'keywords1'
        unique_together = (('event_id', 'event_title'),)

    def __str__(self):
        return 'keywords1'

class FileUploadForm(forms.Form):
    file_source = forms.FileField()

# User class is built-in
