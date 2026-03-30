from django.urls import path
from .views import *

urlpatterns = [

path('register/', register_view,name="register"),

path('login/', login_view,name="login"),

path('logout/', logout_view,name="logout"),

path('admin-dashboard/',admin_dashboard,name='admin_dashboard'),
path('manage-users/',manage_users,name='manage_users'),
path('manage-restaurants/',manage_restaurants,name='manage_restaurants'),
path('manage-bookings/',manage_bookings,name='manage_bookings'),

]