from django.db import models
from django.db.models import F, ExpressionWrapper, DecimalField, Value, When, Case , Q
from django.contrib.auth.models import User
from django.forms import CharField
from home.models import CustomUser


class TaxRate(models.Model):
    id = models.AutoField(primary_key=True)
    start_date = models.DateField()
    vat_rate = models.DecimalField(max_digits=5, decimal_places=2, default=7)
    citytax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=5)
    full_vat_rate = models.DecimalField(max_digits=5, decimal_places=2, default=12)
    tax_zone = models.CharField(max_length=255, default="DE")

    def __str__(self):
        return f"Steuersätze (ab {self.start_date})"

    class Meta:
        ordering = ["-start_date"]


class Platform(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="platform", null=True, blank=True
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    kundennummer = models.CharField(max_length=255, blank=True)
    tel = models.CharField(max_length=255, blank=True)
    login = models.CharField(max_length=255, blank=True)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class Apartment(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="apartment", null=True, blank=True
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    date_contract = models.DateField()

    def __str__(self):
        return self.name


class Reservation(models.Model):
    PURPOSE_CHOICES = [
        ("holiday", "holiday"),
        ("business", "business"),
        ("no-show", "no-show"),
    ]
    id = models.AutoField(primary_key=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    name = models.CharField(max_length=255)
    lname = models.CharField(max_length=255, blank=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    nationality = models.CharField(max_length=255, blank=True, null=True)
    t_sum = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    commission = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    rech_num = models.CharField(max_length=255, blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    purpose = models.CharField(
        max_length=255, choices=PURPOSE_CHOICES, blank=True, null=True
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="reservation")
    platform = models.ForeignKey(
        Platform, on_delete=models.CASCADE, related_name="reservation", blank=True
    )
    apartment = models.ForeignKey(
        Apartment, on_delete=models.CASCADE, related_name="reservation", blank=True
    )

    def __str__(self):
        return self.name

    def get_applicable_tax_rate(self):
        """Returns the  most recent tax rate applicable for the reservation"""
        try:
            return TaxRate.objects.filter(start_date__lte=self.start_date).latest(
                "start_date"
            )
        except TaxRate.DoesNotExist:
            return None

    def calculate_vat(self):
        tax_rate = self.get_applicable_tax_rate()
        if tax_rate:
            netto_sum = self.t_sum / (1 + (tax_rate.vat_rate / 100))
            return self.t_sum - netto_sum
        return 0

    def calculate_citytax(self):
        tax_rate = self.get_applicable_tax_rate()
        if tax_rate:
            netto_sum = (self.t_sum - self.calculate_vat()) / (
                1 + (tax_rate.citytax_rate / 100))
            return self.t_sum - self.calculate_vat() - netto_sum

        return 0

    def calculate_netto(self):
        """returns the netto sum - without taxes"""
        vat = self.calculate_vat()
        if self.purpose == "holiday":
            citytax = self.calculate_citytax()
            return self.t_sum - citytax - vat
        else:
            return self.t_sum - vat

    def get_platform_address(self):
        return self.platform.address
    
    
class Invoice(models.Model):
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE)


    # @classmethod
    # def invoice(cls):
        
    #     return cls.objects.annotate(
    #         number_of_nights=ExpressionWrapper(
    #             F("end_date") - F("start_date"),
    #             output_field=DecimalField(),
    #         ),
    #         citytax=ExpressionWrapper(
    #             F("calculate_citytax")(),
    #             output_field=DecimalField(),
    #         ),
    #         vat=ExpressionWrapper(
    #             F("calculate_vat")(),
    #             output_field=DecimalField(),
    #         ),
    #         netto=ExpressionWrapper(
    #             F("calculate_netto")(),
    #             output_field=DecimalField(),
    #         ),
    #     )
