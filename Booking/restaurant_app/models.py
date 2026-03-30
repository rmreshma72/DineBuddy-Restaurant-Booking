
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):

    ROLE_CHOICES = (
        ('admin','Admin'),
        ('owner','Restaurant Owner'),
        ('customer','Customer'),
    )
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    role = models.CharField(max_length=20,choices=ROLE_CHOICES)

    def __str__(self):
        return self.user.username

class Restaurant(models.Model):

    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    cuisine = models.CharField(max_length=200)
    image = models.ImageField(upload_to='restaurant_images/')
    description = models.TextField()
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    slot_duration = models.IntegerField(default=15)

    def __str__(self):
        return self.name
    
class RestaurantImage(models.Model):
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE,related_name="images")
    image = models.ImageField(upload_to="restaurant_images/")
    def __str__(self):
        return self.restaurant.name
       
class Table(models.Model):

    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    table_number = models.IntegerField()
    capacity = models.IntegerField()

    def __str__(self):
        return f"Table {self.table_number}"
    
class TimeSlot(models.Model):

    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    meal_type = models.CharField(max_length=20)
    time = models.TimeField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.restaurant.name} - {self.meal_type} {self.time}"
    
class Booking(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    table = models.ForeignKey(Table,on_delete=models.CASCADE, null=True, blank=True)
    timeslot = models.ForeignKey(TimeSlot,on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField()
    guests = models.IntegerField()
    status = models.CharField(max_length=20,default="confirmed")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.restaurant.name}"


CATEGORY_CHOICES = [
        ('Breakfast','Breakfast'),
        ('Lunch','Lunch'),
        ('Dinner','Dinner'),
        ('Snacks','Snacks'),
        ('Drinks','Drinks'),
        ('Desserts','Desserts'),
        ]

class Menu(models.Model):

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='menu_images/', null=True, blank=True)
    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"

class Review(models.Model):

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()   # 1 to 5 stars
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.restaurant.name}"


class Offer(models.Model):

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    description = models.TextField()

    discount = models.CharField(max_length=50)

    valid_from = models.TimeField()
    valid_to = models.TimeField()

    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.restaurant.name} - {self.title}"