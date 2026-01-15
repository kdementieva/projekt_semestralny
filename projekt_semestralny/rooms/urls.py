from django.urls import path
from . import views
from .views import rooms_list

urlpatterns = [
  path("", rooms_list, name="room_list"),
]