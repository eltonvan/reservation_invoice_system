from django.contrib import admin
from . import models
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('name',)
 


admin.site.register(models.Reservation , ReservationAdmin)
