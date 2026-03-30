from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
path('home/',home,name='home'),
path('restaurants/',restaurant_list,name="restaurant_list"),
path('restaurant/<int:restaurant_id>/',restaurant_detail,name="restaurant_detail"),
path('owner-dashboard/',owner_dashboard,name='owner_dashboard'),
path('owner-restaurants/',owner_restaurants,name='owner_restaurants'),

path('add-restaurant/',add_restaurant,name="add_restaurant"),
path('edit-restaurant/<int:id>/',edit_restaurant,name="edit_restaurant"),
path('delete-restaurant/<int:id>/',delete_restaurant,name="delete_restaurant"),

path('add-image/<int:id>/',add_restaurant_image,name="add_restaurant_image"),

path('add-menu',add_menu, name="add_menu"),
path('manage-menu/', manage_menu, name='manage_menu'),
path('edit-menu/<int:menu_id>/', edit_menu, name='edit_menu'),
path('delete-menu/<int:menu_id>/', delete_menu, name='delete_menu'),

path('add-table/',add_table,name='add_table'),
path('manage-tables/', manage_tables, name='manage_tables'),

path('add-timeslot/',add_timeslot,name='add_timeslot'),
path('manage-timeslots/',manage_timeslots,name='manage_timeslots'),
path('generate-slots',generate_slots,name = 'generate_slots'),

path('add-review<int:restaurant_id>',add_review,name='add_review'),

path('owner/manage-offers/',manage_offers_restaurants,name = 'manage_offers_restaurants'),
path('restaurant/<int:restaurant_id>/add-offer/', add_offer, name="add_offer"),
path('restaurant/<int:restaurant_id>/offers/', manage_offers, name="manage_offers"),
path('delete-offer/<int:offer_id>/', delete_offer, name="delete_offer"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)