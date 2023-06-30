from django.db import models
from django.contrib.auth.models import User

class Platform(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='platform', null=True, blank=True)
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    kundennummer = models.CharField(max_length=255, blank=True, null=True)
    tel = models.CharField(max_length=255,blank=True, null=True)
    login = models.CharField(max_length=255,blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class Apartment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='apartment', null=True, blank=True)
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    date_contract = models.DateField()

    def __str__(self):
        return self.name



class Reservation(models.Model):

    PURPOSE_CHOICES = [
        ('holiday', 'holiday'),
        ('business', 'business'),
        ('no-show', 'no-show'),
    ]
    id = models.AutoField(primary_key=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    name = models.CharField(max_length=255)
    lname = models.CharField(max_length=255, blank=True, null=True)
    company = models.CharField(max_length=255 , blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    t_sum = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    commission = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    rech_num = models.CharField(max_length=255, blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    purpose = models.CharField(max_length=255,choices=PURPOSE_CHOICES, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservation')
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE, related_name='reservation', blank=True, null=True)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='reservation', blank=True, null=True)

    def __str__(self):
        return self.name    