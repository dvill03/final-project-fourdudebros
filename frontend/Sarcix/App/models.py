from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
#class
class Run(models.Model):

    event_name = models.CharField(max_length=100, blank=False)
    coverage_name = models.CharField(max_length=100, blank=False)
    cover_score = models.DecimalField(default=0, validators=[MinValueValidator(0), MaxValueValidator(2)], decimal_places=2, max_digits=3)

    def __str__(self):
        return 'event_name: {0} coverage_name: {1}'.format(self.event_name, self.coverage_name)
