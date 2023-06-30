from django.db import models
from django.contrib.auth.models import User

class Reservation(models.Model):
    id = models.AutoField(primary_key=True)
    start_date = models.DateField(blank=True, null=True)
    name = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    t_sum = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservation')

