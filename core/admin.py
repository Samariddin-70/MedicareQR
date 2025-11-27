from django.contrib import admin

from core.models.models import Route, Vehicle, Trip, Ticket, TicketValidation


# Register your models here.

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('start_point', 'end_point', 'distance_km', 'estimated_time')
    search_fields = ('name',)
    list_filter = ('name',)

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ("license_plate", "vehicle_type", "capacity", "driver_name", "is_active")
    search_fields = ("vehicle_type",)


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ("route", "vehicle", "departure_time", "arrival_time", "price")
    search_fields = ('number',)


admin.site.register(Ticket)
admin.site.register(TicketValidation)