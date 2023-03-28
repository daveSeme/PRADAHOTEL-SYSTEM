from django.contrib import admin

# Register your models here.

from .models import Booking, Rooms, Availability, CustomUser, Profile

admin.site.register(Booking)
admin.site.register(Rooms)
admin.site.register(Availability)
admin.site.register(CustomUser)
admin.site.register(Profile)