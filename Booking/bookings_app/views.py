from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from restaurant_app.forms import BookingForm
from restaurant_app.models import Restaurant,Booking,TimeSlot,Table
from django.http import JsonResponse
from datetime import date
from django.contrib import messages

@login_required
def book_table(request, restaurant_id):

    restaurant = Restaurant.objects.get(id=restaurant_id)
    timeslots = TimeSlot.objects.filter(
        restaurant=restaurant
    ).order_by("time")
    tables_count = Table.objects.filter(restaurant=restaurant).count()
    date = request.POST.get("date") if request.method == "POST" else None
    slot_status = {}

    for slot in timeslots:
        if date:
            bookings = Booking.objects.filter(
                restaurant=restaurant,
                timeslot=slot,
                date=date
            ).count()
        else:
            bookings = 0
        slot_status[slot.id] = bookings >= tables_count

    if request.method == "POST":
        guests = int(request.POST.get("guests"))
        timeslot_id = request.POST.get("timeslot")
        timeslot = TimeSlot.objects.get(id=timeslot_id)
        tables = Table.objects.filter(
            restaurant=restaurant,
            capacity__gte=guests
        )
        for table in tables:
            if not Booking.objects.filter(
                table=table,
                date=date,
                timeslot=timeslot
            ).exists():
                Booking.objects.create(
                    user=request.user,
                    restaurant=restaurant,
                    table=table,
                    timeslot=timeslot,
                    date=date,
                    guests=guests
                )

                return redirect("booking_success")
        return render(request, "customer/book_table.html", {
            "restaurant": restaurant,
            "timeslots": timeslots,
            "slot_status": slot_status,
            "error": "No table available for this slot"
        })
    return render(request, "customer/book_table.html", {
        "restaurant": restaurant,
        "timeslots": timeslots,
        "slot_status": slot_status
    })


@login_required
def my_bookings(request):

    bookings = Booking.objects.filter(user=request.user)

    return render(request,'customer/my_bookings.html',{
        'bookings':bookings
    })

@login_required
def booking_detail(request,id):

    booking = get_object_or_404(Booking,id=id,user=request.user)

    return render(request,'customer/booking_detail.html',{
        'booking':booking
    })


@login_required
def cancel_booking(request, booking_id):

    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if booking.date < date.today():
     return redirect('my_bookings')

    booking.status = "cancelled"
    booking.save()

    messages.success(request, "Booking cancelled successfully!")

    return redirect('my_bookings')

@login_required
def booking_success(request):
    return render(request, 'customer/booking_success.html')

@login_required
def view_bookings(request):

    bookings = Booking.objects.filter(restaurant__owner=request.user)

    return render(request,'owner/view_bookings.html',{'bookings':bookings})

def get_available_tables(request):

    restaurant_id = request.GET.get('restaurant_id')
    timeslot_id = request.GET.get('timeslot_id')
    date = request.GET.get('date')

    tables = Table.objects.filter(restaurant_id=restaurant_id)

    booked_tables = Booking.objects.filter(
        timeslot_id=timeslot_id,
        date=date
    ).values_list('table_id', flat=True)

    available_tables = tables.exclude(id__in=booked_tables)

    data = []

    for table in available_tables:
        data.append({
            'id': table.id,
            'name': f"Table {table.table_number} (Seats {table.capacity})"
        })

    return JsonResponse(data, safe=False)





