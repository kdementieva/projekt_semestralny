from django import forms
from .models import Reservation, Room
from django.core.exceptions import ValidationError
from datetime import timedelta
from django.utils import timezone

class ReservationForm(forms.ModelForm):
  class Meta:
    model = Reservation
    fields = ['room', 'reservation_time_start', 'reservation_time_end']
    labels = {
      'room': 'Sala',
      'reservation_time_start': 'Początek rezerwacji',
      'reservation_time_end': 'Koniec rezerwacji',
    }
    widgets = {
      'reservation_time_start': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
      'reservation_time_end': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
    }

  def clean(self):
    cleaned_data = super().clean()
    room = cleaned_data.get('room')
    start = cleaned_data.get('reservation_time_start')
    end = cleaned_data.get('reservation_time_end')
    now = timezone.now()

    if not start or not end:
      return cleaned_data

    if start < now:
      raise ValidationError("Nie można rezerwować terminu w przeszłości.")

    if end < now:
      raise ValidationError("Data zakończenia nie może być w przeszłości.")

    if end <= start:
      raise ValidationError("Data zakończenia musi być późniejsza niż data rozpoczęcia.")

    duration = end - start

    if duration < timedelta(hours=1):
      raise ValidationError("Minimalny czas rezerwacji to 1 godzina.")

    if duration > timedelta(hours=24):
      raise ValidationError("Maksymalny czas rezerwacji to 24 godziny.")

    collision = Reservation.objects.filter(
      room=room,
      status__in=['pending', 'approved'],
      reservation_time_start__lt=end,
      reservation_time_end__gt=start,
    ).exists()

    if collision:
      raise ValidationError(
        "Wybrany termin jest niedostępny — sala jest już zarezerwowana."
      )

    return cleaned_data


class RoomForm(forms.ModelForm):
  class Meta:
    model = Room
    fields = ['name', 'description', 'price']
    labels = {
      'name': 'Nazwa sali',
      'description': 'Opis',
      'price': 'Cena (PLN)',
    }
