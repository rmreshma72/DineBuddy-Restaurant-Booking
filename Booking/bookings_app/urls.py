from django.urls import path
from .views import *


urlpatterns = [

path('book/<int:restaurant_id>/',book_table,name="book_table"),

path('my-bookings/',my_bookings,name="my_bookings"),

path('booking/<int:id>/',booking_detail,name="booking_detail"),

path('cancel-booking/<int:booking_id>/',cancel_booking,name="cancel_booking"),

path('get-available-tables/', get_available_tables, name='get_available_tables'),

path('booking-success/', booking_success, name='booking_success'),

path('owner/bookings/',view_bookings,name='view_bookings'),

]