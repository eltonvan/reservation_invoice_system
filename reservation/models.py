from django.db import models
from django.contrib.auth.models import User
from django.forms import CharField
from home.models import CustomUser


class TaxRate(models.Model):
    user = models.ForeignKey(
    CustomUser,
    on_delete=models.CASCADE,
    related_name="taxrates",
    null=True,
    blank=True,
    )
    start_date = models.DateField()
    vat_rate = models.DecimalField(max_digits=5, decimal_places=2, default=7)
    citytax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=5)
    full_vat_rate = models.DecimalField(max_digits=5, decimal_places=2, default=19)
    tax_zone = models.CharField(max_length=255, default="Germany")

    def __str__(self):
       # return f"Steuersätze (ab {self.start_date}, {self.tax_zone}, {self.vat_rate}%, {self.citytax_rate}%)"
        return self.tax_zone
    class Meta:
        ordering = ["-start_date"]


class Platform(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="platform",
        null=True,
        blank=True,
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
        CustomUser,
        on_delete=models.CASCADE,
        related_name="apartment",
        null=True,
        blank=True,
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
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    name = models.CharField(max_length=255)
    lname = models.CharField(max_length=255, blank=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    number_of_guests = models.IntegerField(blank=True)
    nationality = models.CharField(max_length=255, blank=True, null=True)
    t_sum = models.DecimalField(max_digits=10, decimal_places=2)
    commission = models.DecimalField(
        max_digits=10, decimal_places=2
    )
    rech_num = models.CharField(max_length=255, blank=True)
    link = models.URLField(blank=True, null=True)
    purpose = models.CharField(
        max_length=255, choices=PURPOSE_CHOICES, blank=True
    )
    comment = models.TextField(blank=True, null=True)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="reservation"
    )
    platform = models.ForeignKey(
        Platform, on_delete=models.CASCADE, related_name="reservation"
    )
    apartment = models.ForeignKey(
        Apartment, on_delete=models.CASCADE, related_name="reservation"
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # if not self.user:  
        #     self.user = CustomUser.objects.get(pk=self.request.user.pk)
        #     self.save() 

        invoice_id = self.id
        invoice = Invoice(
            id=invoice_id,
            name=self.name,
            invoice_netto=self.calculate_netto(),
            invoice_vat=self.calculate_vat(),
            invoice_citytax=self.calculate_citytax(),
            invoice_number_of_nights=self.number_of_nights(),
            reservation=self,
        )
        invoice.save()

    def get_applicable_tax_rate(self):
        """Returns the  most recent tax rate applicable for the reservation"""
        try:
            result = TaxRate.objects.filter(start_date__lte=self.start_date).latest(
                "start_date"
            )
            print(result)
            return result

        except TaxRate.DoesNotExist:
            print("No tax rate found")
            return None

    def calculate_vat(self):
        tax_rate = self.get_applicable_tax_rate()
        if tax_rate:
            sum_no_vat = self.t_sum / (1 + (tax_rate.vat_rate / 100))
            return self.t_sum - sum_no_vat
        return 0

    def calculate_citytax(self):
        tax_rate = self.get_applicable_tax_rate()
        if tax_rate:
            sum_no_vat = self.t_sum / (1 + (tax_rate.vat_rate / 100))
            sum_no_vat_no_citytax = (self.t_sum - self.calculate_vat()) / (
                1 + (tax_rate.citytax_rate / 100)
            )
            return sum_no_vat - sum_no_vat_no_citytax

        return 0

    def calculate_netto(self):
        """returns the netto sum - without taxes"""
        vat = self.calculate_vat()
        if self.purpose == "holiday":
            citytax = self.calculate_citytax()
            return self.t_sum - citytax - vat
        else:
            return self.t_sum - vat
        
    def number_of_nights(self):
        """returns the number of nights"""
        return (self.end_date - self.start_date).days
    

    def get_platform_address(self):
        return self.platform.address


class Invoice(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    invoice_netto = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    reservation = models.ForeignKey(
        Reservation, on_delete=models.CASCADE, related_name="invoices"
    )
    invoice_vat = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    invoice_citytax = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    invoice_number_of_nights = models.IntegerField(blank=True, null=True)

