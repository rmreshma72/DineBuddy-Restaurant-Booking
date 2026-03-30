from django.contrib import admin
from .models import Restaurant, Table, Booking, TimeSlot, Menu, RestaurantImage, Review, Offer

class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('restaurant','meal_type','time')



admin.site.register(Restaurant)
admin.site.register(Table)
admin.site.register(Booking)
admin.site.register(TimeSlot, TimeSlotAdmin)
admin.site.register(Menu)
admin.site.register(RestaurantImage)
admin.site.register(Review)
admin.site.register(Offer)
