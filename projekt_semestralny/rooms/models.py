from django.db import models
from django.conf import settings


class Room(models.Model):
  name = models.CharField(max_length=50, verbose_name="Nazwa sali")
  description = models.CharField(max_length=200, verbose_name="Opis")
  price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Cena (PLN)")

  def __str__(self):
    return self.name

  class Meta:
    verbose_name = "Sala"
    verbose_name_plural = "Sale"


class Reservation(models.Model):
  STATUS_CHOICES = [
    ('pending', 'Oczekująca'),
    ('approved', 'Zatwierdzona'),
    ('cancelled', 'Anulowana'),
  ]

  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Użytkownik")
  room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="reservations", verbose_name="Sala")
  reservation_time_start = models.DateTimeField(verbose_name="Początek rezerwacji")
  reservation_time_end = models.DateTimeField(verbose_name="Koniec rezerwacji")
  status = models.CharField( max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Status")

  def __str__(self):
    return (
      f"{self.room} | "
      f"{self.reservation_time_start} – {self.reservation_time_end}"
    )

  class Meta:
    verbose_name = "Rezerwacja"
    verbose_name_plural = "Rezerwacje"
