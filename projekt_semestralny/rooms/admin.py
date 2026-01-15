from django.contrib import admin
from . import models

@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
  list_display = ['name', 'description', 'price']
  search_fields = ['name',]

@admin.register(models.Reservation)
class ReservationAdmin(admin.ModelAdmin):
  list_display = ['user', 'room', 'reservation_time_start', 'reservation_time_end', 'status']
  list_filter = ['status', 'room']
  search_fields = ['user__username', 'room__name']
  ordering = ['-reservation_time_start']