from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from restaurant_app.models import UserProfile,Restaurant,Booking
from restaurant_app.forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from datetime import date
import json

def register_view(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            password = form.cleaned_data['password']
            role = form.cleaned_data['role']

            user.set_password(password)
            user.save()

            # Create profile
            UserProfile.objects.create(
                user=user,
                role=role
            )

            return redirect('login')

    else:

        form = RegisterForm()

    return render(request,'register.html',{
        'form':form
    })


def login_view(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:

            login(request, user)

            profile, created = UserProfile.objects.get_or_create(user=user)

            if user.is_superuser:
                return redirect('admin_dashboard')

            elif profile.role == "owner":
                return redirect('owner_dashboard')

            else:
                return redirect('home')

    return render(request,'login.html')

def logout_view(request):

    logout(request)

    return redirect('login')

@login_required
def admin_dashboard(request):

    # Total counts
    total_users = User.objects.count()
    total_restaurants = Restaurant.objects.count()
    total_bookings = Booking.objects.count()

    # Today's bookings
    today_bookings = Booking.objects.filter(
        date=date.today()
    ).count()

    # BOOKINGS PER DAY
    bookings_per_day = Booking.objects.values('date').annotate(
        total=Count('id')
    ).order_by('date')

    days = [str(b['date']) for b in bookings_per_day]
    day_counts = [b['total'] for b in bookings_per_day]

    # MOST POPULAR RESTAURANT
    popular_restaurant = Booking.objects.values(
        'restaurant__name'
    ).annotate(
        total=Count('id')
    ).order_by('-total').first()

    context = {
        "total_users": total_users,
        "total_restaurants": total_restaurants,
        "total_bookings": total_bookings,
        "today_bookings": today_bookings,
        "popular_restaurant": popular_restaurant,
        "days": json.dumps(days),
        "day_counts": json.dumps(day_counts)
    }

    return render(request, "admin/admin_dashboard.html", context)

@login_required
def manage_users(request):

    users = User.objects.all()

    return render(request,'admin/manage_users.html',{
        'users':users
    })

@login_required
def manage_restaurants(request):

    restaurants = Restaurant.objects.all()

    return render(request,'admin/manage_restaurants.html',{
        'restaurants':restaurants
    })

def manage_bookings(request):
    bookings = Booking.objects.all()

    return render(request,'admin/manage_bookings.html',{
        'bookings':bookings
    })