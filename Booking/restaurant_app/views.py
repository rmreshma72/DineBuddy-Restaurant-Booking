from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Restaurant,RestaurantImage,Booking,Table,TimeSlot,Menu,Review,Offer
from .forms import RestaurantForm,MenuForm
from django.db.models import Q
from datetime import date
from django.db.models import Count
import json  



def home(request):
    restaurants = Restaurant.objects.all()
    return render(request,'home.html',{'restaurants':restaurants})

def restaurant_list(request):

    query = request.GET.get('q')
    location = request.GET.get('location')

    restaurants = Restaurant.objects.all()

    if query:
        restaurants = restaurants.filter(
            Q(name__icontains=query) |
            Q(cuisine__icontains=query)
        )

    if location:
        restaurants = restaurants.filter(location__icontains=location)

    return render(request,'customer/restaurant_list.html',{
        'restaurants':restaurants,
        'query':query
    })

def restaurant_detail(request, restaurant_id):

    restaurant = Restaurant.objects.get(id=restaurant_id)
    images = restaurant.images.all()
    menu_items = Menu.objects.filter(restaurant=restaurant)
    reviews = Review.objects.filter(restaurant=restaurant)
    offers = Offer.objects.filter(
        restaurant = restaurant,
        active = True
    )

    return render(request,'customer/restaurant_detail.html',{
        'restaurant':restaurant,
        'images':images,
        'menu_items':menu_items,
        'reviews':reviews,
        'offers' :offers
    })

@login_required
def add_restaurant(request):

    if request.method == "POST":

        name = request.POST.get('name')
        location = request.POST.get('location')
        cuisine = request.POST.get('cuisine')
        description = request.POST.get('description')
        opening_time = request.POST.get('opening_time')
        closing_time = request.POST.get('closing_time')
        image = request.FILES.get('image')

        Restaurant.objects.create(
            owner=request.user,
            name=name,
            location=location,
            cuisine=cuisine,
            description=description,
            opening_time=opening_time,
            closing_time=closing_time,
            image=image
        )

        return redirect('owner_dashboard')

    return render(request,'owner/add_restaurant.html')

@login_required
def owner_dashboard(request):

    restaurants = Restaurant.objects.filter(owner=request.user)
    
    bookings = Booking.objects.filter(restaurant__in=restaurants)
    
    # Bookings per day
    bookings_per_day = bookings.values('date').annotate(
        total = Count('id')
    ).order_by('date')

    days = [str(b['date']) for b in bookings_per_day]
    day_counts = [b['total'] for b in bookings_per_day]

    # PEAK HOURS
    peak_hours = bookings.values('timeslot__time').annotate(
        total=Count('id')
    ).order_by('timeslot__time')

    hours = [str(p['timeslot__time']) for p in peak_hours]
    hour_counts = [p['total'] for p in peak_hours]

    # TABLE UTILIZATION
    tables = Table.objects.filter(restaurant__in=restaurants).count()
    total_bookings = bookings.count()

    #Total Bookings
    total_bookings = Booking.objects.filter(restaurant__in = restaurants).count()
    
    #Today's Bookings
    today_bookings = Booking.objects.filter(
        restaurant__in = restaurants,
        date =date.today()
                ).count()
    
    #Most booked Timeslot
    popular_slot = Booking.objects.filter(
        restaurant__in = restaurants
    ).values('timeslot__time').annotate(
        total = Count('id')
    ).order_by('-total').first()

    context ={
        "restaurants" : restaurants,
        'bookings':bookings,
        "days": json.dumps(days),
        "day_counts": json.dumps(day_counts),
        "hours": json.dumps(hours),
        "hour_counts": json.dumps(hour_counts),
        "tables": tables,
        "total_bookings": total_bookings,
        "today_bookings": today_bookings,
        "popular_slot" : popular_slot
    }

    return render(request,'owner/owner_dashboard.html',context)

@login_required
def owner_restaurants(request):

    restaurants = Restaurant.objects.filter(owner=request.user)

    return render(request,'owner/owner_restaurants.html',{
        'restaurants':restaurants
    })

@login_required
def edit_restaurant(request,id):

    restaurant = get_object_or_404(Restaurant,id=id,owner=request.user)

    if request.method == "POST":

        form = RestaurantForm(request.POST,request.FILES,instance=restaurant)

        if form.is_valid():
            form.save()
            return redirect('owner_dashboard')
    else:
        form = RestaurantForm(instance=restaurant)

    return render(request,'owner/edit_restaurant.html',{
        'form':form
    })

@login_required
def delete_restaurant(request,id):

    restaurant = get_object_or_404(Restaurant,id=id,owner=request.user)

    restaurant.delete()

    return redirect('owner_dashboard')

@login_required
def add_restaurant_image(request,id):

    restaurant = get_object_or_404(Restaurant,id=id,owner=request.user)
    if request.method == "POST":
        image = request.FILES.get('image')
        RestaurantImage.objects.create(
            restaurant=restaurant,
            image=image
        )
        return redirect('owner_dashboard')
    return render(request,'owner/add_image.html',{
        'restaurant':restaurant
    })




#--------------------------table-------------------------------------
@login_required
def add_table(request):

    restaurants = Restaurant.objects.filter(owner=request.user)

    if request.method == "POST":

        restaurant_id = request.POST.get('restaurant')
        number = request.POST.get('number')
        capacity = request.POST.get('capacity')

        restaurant = Restaurant.objects.get(id=restaurant_id)

        Table.objects.create(
            restaurant=restaurant,
            table_number=number,
            capacity=capacity
        )

        return redirect('manage_tables')

    return render(request,'owner/add_table.html',{'restaurants':restaurants})

@login_required
def manage_tables(request):

    restaurant = Restaurant.objects.filter(owner=request.user).first()

    tables = Table.objects.filter(restaurant=restaurant)

    if request.method == "POST":

        table_number = request.POST.get('table_number')
        capacity = request.POST.get('capacity')

        Table.objects.create(
            restaurant=restaurant,
            table_number=table_number,
            capacity=capacity
        )

        return redirect('manage_tables')

    return render(request,'owner/manage_tables.html',{
        'tables':tables
    })


#-------------------------timeslots--------------------------------


from datetime import datetime, timedelta
from .models import TimeSlot, Restaurant


def generate_slots(restaurant):

    start = datetime.combine(datetime.today(), restaurant.opening_time)
    end = datetime.combine(datetime.today(), restaurant.closing_time)

    duration = restaurant.slot_duration

    while start <= end:

        TimeSlot.objects.get_or_create(
            restaurant=restaurant,
            time=start.time()
        )

        start += timedelta(minutes=duration)


def create_slots(request):

    restaurants = Restaurant.objects.all()

    if request.method == "POST":

        restaurant_id = request.POST.get("restaurant")
        meal_type = request.POST.get("meal_type")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")
        interval = int(request.POST.get("interval"))

        restaurant = Restaurant.objects.get(id=restaurant_id)

        generate_slots(
            restaurant,
            meal_type,
            start_time,
            end_time,
            interval
        )

        return redirect("owner_dashboard")

    return render(request, "owner/create_slots.html",{
        "restaurants":restaurants
    })


@login_required
def add_timeslot(request):

    restaurants = Restaurant.objects.filter(owner=request.user)

    if request.method == "POST":

        restaurant_id = request.POST.get('restaurant')
        meal_type = request.POST.get('meal_type')
        time = request.POST.get('slot')

        restaurant = Restaurant.objects.get(id=restaurant_id)

        TimeSlot.objects.create(
            restaurant=restaurant,
            meal_type=meal_type,
            time=time
        )

        return redirect('manage_timeslots')

    return render(request,'owner/add_timeslot.html',{
        'restaurants':restaurants
    })

@login_required
def manage_timeslots(request):

    timeslots = TimeSlot.objects.filter(restaurant__owner=request.user)

    return render(request,'owner/manage_timeslots.html',{
        'timeslots':timeslots
    })



# ----------------------------MENU-----------------------------------

def add_menu(request):

    # Only owner's restaurants
    restaurants = Restaurant.objects.filter(owner=request.user)

    if request.method == "POST":

        form = MenuForm(request.POST, request.FILES)

        if form.is_valid():

            menu = form.save(commit=False)

            # ✅ get restaurant from dropdown
            restaurant_id = request.POST.get('restaurant')

            try:
                restaurant = Restaurant.objects.get(
                    id=restaurant_id,
                    owner=request.user   # 🔐 security
                )
            except Restaurant.DoesNotExist:
                return render(request, 'owner/add_menu.html', {
                    'form': form,
                    'restaurants': restaurants,
                    'error': 'Invalid restaurant selected'
                })

            menu.restaurant = restaurant
            menu.save()

            return redirect('manage_menu')

        else:
            print(form.errors)  # 🔍 debug

    else:
        form = MenuForm()

    return render(request, 'owner/add_menu.html', {
        'form': form,
        'restaurants': restaurants
    })



@login_required
def manage_menu(request):

    menus = Menu.objects.filter(restaurant__owner=request.user)

    return render(request, 'owner/manage_menu.html', {
        'menus': menus
    })

@login_required
def edit_menu(request, menu_id):

    menu = Menu.objects.get(id=menu_id, restaurant__owner=request.user)

    if request.method == "POST":
        form = MenuForm(request.POST, request.FILES, instance=menu)

        if form.is_valid():
            form.save()
            return redirect('manage_menu')
        else:
            print(form.errors)

    else:
        form = MenuForm(instance=menu)

    return render(request, 'owner/edit_menu.html', {
        'form': form
        })


@login_required
def delete_menu(request, menu_id):
    
    menu = Menu.objects.get(id=menu_id, restaurant__owner=request.user)
    menu.delete()
    return redirect('manage_menu')

# ----------------Review------------------

@login_required
def add_review(request, restaurant_id):

    restaurant = Restaurant.objects.get(id=restaurant_id)
    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")
        Review.objects.create(
            restaurant=restaurant,
            user=request.user,
            rating=rating,
            comment=comment
        )
        return redirect("restaurant_detail", restaurant_id=restaurant.id)

# ---------------------Offer------------------
def manage_offers_restaurants(request):
    restaurants = Restaurant.objects.filter(owner = request.user)

    return render(request,
                  "owner/owner_offers_restaurants.html",
                  {"restaurants":restaurants}
                  )

@login_required
def manage_offers(request, restaurant_id):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    offers = Offer.objects.filter(restaurant = restaurant)
    context = {
        "restaurant" : restaurant,
        "offers" : offers
    }
    return render(request, "owner/manage_offers.html", context)


@login_required
def add_offer(request, restaurant_id):

    restaurant = Restaurant.objects.get(id=restaurant_id)

    if request.method == "POST":

        Offer.objects.create(
            restaurant=restaurant,
            title=request.POST.get("title"),
            description=request.POST.get("description"),
            discount=request.POST.get("discount"),
            valid_from=request.POST.get("valid_from"),
            valid_to=request.POST.get("valid_to"),
        )

        return redirect("manage_offers",restaurant_id = restaurant.id)

    return render(request,"owner/add_offer.html",{"restaurant":restaurant})


@login_required
def delete_offer(request, offer_id):
    offer = Offer.objects.get(id = offer_id)
    restaurant_id = offer.restaurant.id

    offer.delete()
    return redirect("manage_offers", restaurant_id = restaurant_id)