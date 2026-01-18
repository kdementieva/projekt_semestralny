from django.shortcuts import render, redirect, get_object_or_404
from .models import Room, Reservation
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import ReservationForm, RoomForm
from django.contrib import messages


def rooms_list(request):
  rooms = Room.objects.all()
  return render(request, 'rooms/room_list.html', {'rooms': rooms})


@login_required
def create_reservation(request):
  if request.method == 'POST':
    form = ReservationForm(request.POST)
    if form.is_valid():
      reservation = form.save(commit=False)
      reservation.user = request.user
      reservation.status = 'pending'
      reservation.save()
      messages.success(request, "Rezerwacja została utworzona.")
      return redirect('room_list')
  else:
    form = ReservationForm()

  return render(request, 'rooms/reservation_form.html', {'form': form})


@login_required
def my_reservation(request):
  reservations = Reservation.objects.filter(user=request.user).order_by('-reservation_time_start')

  return render(request, 'rooms/my_reservations.html', {'reservations': reservations})


@login_required
def edit_reservation(request, reservation_id):
  reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)

  if reservation.status != 'pending':
    messages.error(request, "Nie można edytować tej rezerwacji.")
    return redirect('my_reservations')

  if request.method == 'POST':
    form = ReservationForm(request.POST, instance=reservation)
    if form.is_valid():
      form.save()
      messages.success(request, "Rezerwacja została zaktualizowana.")
      return redirect('my_reservations')
  else:
    form = ReservationForm(instance=reservation)

  return render(request, 'rooms/reservation_form.html', {'form': form, 'edit': True})


@login_required
def cancel_reservation(request, reservation_id):
  reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)

  if reservation.status != 'pending':
    messages.error(request, "Nie można anulować tej rezerwacji.")
  else:
    reservation.status = 'cancelled'
    reservation.save()
    messages.success(request, "Rezerwacja została anulowana.")

  return redirect('my_reservations')


@staff_member_required
def admin_reservations(request):
  reservations = Reservation.objects.all().order_by('-reservation_time_start')
  return render(request, 'rooms/admin_reservations.html', {'reservations': reservations})


@staff_member_required
def approve_reservation(request, reservation_id):
  reservation = get_object_or_404(Reservation, id=reservation_id)
  reservation.status = 'approved'
  reservation.save()
  messages.success(request, "Rezerwacja została zatwierdzona.")
  return redirect('admin_reservations')


@staff_member_required
def reject_reservation(request, reservation_id):
  reservation = get_object_or_404(Reservation, id=reservation_id)
  reservation.status = 'cancelled'
  reservation.save()
  messages.success(request, "Rezerwacja została odrzucona.")
  return redirect('admin_reservations')


@staff_member_required
def admin_dashboard(request):
  return render(request, 'rooms/admin_dashboard.html',
    {
      'total': Reservation.objects.count(),
      'pending': Reservation.objects.filter(status='pending').count(),
      'approved': Reservation.objects.filter(status='approved').count(),
      'cancelled': Reservation.objects.filter(status='cancelled').count(),
    })


@staff_member_required
def admin_rooms(request):
  rooms = Room.objects.all()
  return render(request, 'rooms/admin_rooms.html', {'rooms': rooms})


@staff_member_required
def admin_room_create(request):
  if request.method == 'POST':
    form = RoomForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request, "Sala została dodana.")
      return redirect('admin_rooms')
  else:
    form = RoomForm()

  return render(request, 'rooms/admin_room_form.html', {'form': form, 'create': True})


@staff_member_required
def admin_room_edit(request, room_id):
  room = get_object_or_404(Room, id=room_id)

  if request.method == 'POST':
    form = RoomForm(request.POST, instance=room)
    if form.is_valid():
      form.save()
      messages.success(request, "Dane sali zostały zaktualizowane.")
      return redirect('admin_rooms')
  else:
    form = RoomForm(instance=room)

  return render(request, 'rooms/admin_room_form.html', {'form': form, 'create': False})


@staff_member_required
def admin_room_delete(request, room_id):
  room = get_object_or_404(Room, id=room_id)

  if request.method == 'POST':
    room.delete()
    messages.success(request, "Sala została usunięta.")

  return redirect('admin_rooms')
