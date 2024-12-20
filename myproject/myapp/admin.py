from django.contrib import admin
from .models import GamePark, SearchDeal, Manager, Location, PlaceToVisit, Hotel, Booking

# Registering the existing models with the admin site
admin.site.register(GamePark)
admin.site.register(SearchDeal)
admin.site.register(Manager)
admin.site.register(Location)
admin.site.register(PlaceToVisit)
admin.site.register(Hotel)

# Registering the Booking model
admin.site.register(Booking)
