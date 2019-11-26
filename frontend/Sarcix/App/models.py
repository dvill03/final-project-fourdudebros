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

class Naive(models.Model):
    run_name = models.TextField(primary_key=True)
    event_name = models.TextField()
    b = models.DecimalField(max_digits=3, decimal_places=2)
    c = models.DecimalField(max_digits=3, decimal_places=2)
    d = models.DecimalField(max_digits=3, decimal_places=2)
    e = models.DecimalField(max_digits=3, decimal_places=2)
    f = models.DecimalField(max_digits=3, decimal_places=2)
    g = models.DecimalField(max_digits=3, decimal_places=2)
    h = models.DecimalField(max_digits=3, decimal_places=2)
    i = models.DecimalField(max_digits=3, decimal_places=2)
    j = models.DecimalField(max_digits=3, decimal_places=2)
    k = models.DecimalField(max_digits=3, decimal_places=2)
    l = models.DecimalField(max_digits=3, decimal_places=2)
    m = models.DecimalField(max_digits=3, decimal_places=2)
    n = models.DecimalField(max_digits=3, decimal_places=2)
    o = models.DecimalField(max_digits=3, decimal_places=2)
    p = models.DecimalField(max_digits=3, decimal_places=2)
    q = models.DecimalField(max_digits=3, decimal_places=2)
    r = models.DecimalField(max_digits=3, decimal_places=2)
    s = models.DecimalField(max_digits=3, decimal_places=2)
    t = models.DecimalField(max_digits=3, decimal_places=2)
    u = models.DecimalField(max_digits=3, decimal_places=2)
    v = models.DecimalField(max_digits=3, decimal_places=2)
    w = models.DecimalField(max_digits=3, decimal_places=2)
    x = models.DecimalField(max_digits=3, decimal_places=2)
    y = models.DecimalField(max_digits=3, decimal_places=2)
    z = models.DecimalField(max_digits=3, decimal_places=2)
    aa = models.DecimalField(max_digits=3, decimal_places=2)
    ab = models.DecimalField(max_digits=3, decimal_places=2)
    ac = models.DecimalField(max_digits=3, decimal_places=2)
    ad = models.DecimalField(max_digits=3, decimal_places=2)
    ae = models.DecimalField(max_digits=3, decimal_places=2)
    af = models.DecimalField(max_digits=3, decimal_places=2)
    ag = models.DecimalField(max_digits=3, decimal_places=2)
    ah = models.DecimalField(max_digits=3, decimal_places=2)
    ai = models.DecimalField(max_digits=3, decimal_places=2)
    aj = models.DecimalField(max_digits=3, decimal_places=2)
    ak = models.DecimalField(max_digits=3, decimal_places=2)
    al = models.DecimalField(max_digits=3, decimal_places=2)
    am = models.DecimalField(max_digits=3, decimal_places=2)
    an = models.DecimalField(max_digits=3, decimal_places=2)
    ao = models.DecimalField(max_digits=3, decimal_places=2)
    ap = models.DecimalField(max_digits=3, decimal_places=2)
    aq = models.DecimalField(max_digits=3, decimal_places=2)
    ar = models.DecimalField(max_digits=3, decimal_places=2)
    ass = models.DecimalField(max_digits=3, decimal_places=2)
    att = models.DecimalField(max_digits=3, decimal_places=2)
    au = models.DecimalField(max_digits=3, decimal_places=2)
    av = models.DecimalField(max_digits=3, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'naive'
        unique_together = (('run_name', 'event_name'),)

# User class is built-in
