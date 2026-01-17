from django.urls import path
from . import views
from .views import rooms_list, create_reservation, my_reservation, edit_reservation, cancel_reservation, admin_reservations, reject_reservation, approve_reservation, admin_dashboard, admin_rooms, admin_room_create, admin_room_edit, admin_room_delete

urlpatterns = [
  path("", rooms_list, name="room_list"),
  path('reserve/', create_reservation, name='create_reservation'),
  path('my/', my_reservation, name='my_reservations'),
  path('edit/<int:reservation_id>/', edit_reservation, name='edit_reservation'),
  path('cancel/<int:reservation_id>/', cancel_reservation, name='cancel_reservation'),
  path('admin-panel/', admin_reservations, name='admin_reservations'),
  path('admin-panel/approve/<int:reservation_id>/', approve_reservation, name='approve_reservation'),
  path('admin-panel/reject/<int:reservation_id>/', reject_reservation, name='reject_reservation'),
  path('admin-panel/dashboard/', admin_dashboard, name='admin_dashboard'),
  path('admin-panel/rooms/', admin_rooms, name='admin_rooms'),
  path('admin-panel/rooms/add/', admin_room_create, name='admin_room_create'),
  path('admin-panel/rooms/edit/<int:room_id>/', admin_room_edit, name='admin_room_edit'),
  path('admin-panel/rooms/delete/<int:room_id>/', admin_room_delete, name='admin_room_delete'),
]