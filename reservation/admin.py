from django.contrib import admin
from reservation.models import Reservation, Invoice, TaxRate, Platform, Apartment


class ReservationAdmin(admin.ModelAdmin):
    list_display = ("name",)


admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Invoice)
admin.site.register(TaxRate)
admin.site.register(Platform)
admin.site.register(Apartment)
