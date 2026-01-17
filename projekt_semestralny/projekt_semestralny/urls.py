from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('rooms/', include('rooms.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls'))
]
