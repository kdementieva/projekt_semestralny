from django.shortcuts import render
from .models import Room

def rooms_list(request):
  rooms = Room.objects.all()
  return render(request, 'rooms/room_list.html', {'rooms': rooms})

