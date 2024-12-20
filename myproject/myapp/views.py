from django.shortcuts import render, redirect, get_object_or_404
from .models import GamePark, SearchDeal, Manager, Location, PlaceToVisit, Hotel, Booking
from django.http import JsonResponse
from .models import Hotel
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# views.py

from django.core.mail import send_mail
from django.utils.timezone import now
from datetime import timedelta
from .models import Manager

import random

def generate_otp():
    """Generate a 6-digit random OTP."""
    return str(random.randint(100000, 999999))

def send_otp_email(manager):
    otp = generate_otp()
    manager.otp = otp
    manager.otp_created_at = now()
    manager.save()
    
    subject = 'Your OTP for Login'
    message = f'Your OTP is {otp}. It is valid for 10 minutes.'
    recipient_list = [manager.email]
    
    send_mail(subject, message, 'elyseniyonzima202@gmail.com', recipient_list)

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            manager = Manager.objects.get(email=email)
            if manager.password == password:  # Check if password matches
                # Store manager's ID in session
                request.session['manager_id'] = manager.id

                # Generate OTP and send email
                send_otp_email(manager)  # Send OTP to manager's email
                return redirect('verify_otp')  # Redirect to verify OTP page

            else:
                messages.error(request, 'Incorrect password!')
        except Manager.DoesNotExist:
            messages.error(request, 'Manager not found!')

    return render(request, 'myapp/login.html')

def verify_otp_view(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        manager_id = request.session.get('manager_id')
        
        if not manager_id:
            messages.error(request, 'Session expired. Please log in again.')
            return redirect('login')
        
        try:
            manager = Manager.objects.get(id=manager_id)
            if manager.otp == otp and manager.otp_created_at > now() - timedelta(minutes=10):
                # OTP is valid
                manager.otp = None  # Clear the OTP after successful login
                manager.otp_created_at = None
                manager.save()

                # Set the session to indicate OTP is verified
                request.session['otp_verified'] = True

                # Redirect based on category or default to dashboard
                if manager.category == 'hotel':
                    return redirect('hotels')
                elif manager.category == 'transport':
                    return redirect('transports')
                elif manager.category == 'park':
                    return redirect('parks')
                else:
                    return redirect('dashboard')  # Default to dashboard if no category

            else:
                messages.error(request, 'Invalid or expired OTP.')
        except Manager.DoesNotExist:
            messages.error(request, 'Manager not found!')

    return render(request, 'myapp/verify_otp.html')

def hotels_view(request):
    return render(request, 'myapp/hotels.html')

def transports_view(request):
    return render(request, 'myapp/transports.html')

def parks_view(request):
    return render(request, 'myapp/parks.html')



def get_managers(request):
    managers = Manager.objects.all().values('name', 'email', 'telephone', 'category')  # Fetch necessary fields
    manager_list = list(managers)
    return JsonResponse({'managers': manager_list})

from django.shortcuts import redirect



def logout_view(request):
    try:
        del request.session['manager_id']  # Remove the manager's ID from the session
    except KeyError:
        pass  # If there's no manager_id in session, just pass
    return redirect('login')  # Redirect to login page after logging out
def get_booking_details(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
        data = {
            'name': booking.name,
            'location': booking.location,
            'hotel': booking.hotel,
            'transport': booking.transport,
            'start_date': booking.start_date,
            'end_date': booking.end_date,
        }
        return JsonResponse(data)
    except Booking.DoesNotExist:
        return JsonResponse({'error': 'Booking not found'}, status=404)
def get_booking_details(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    data = {
        'name': booking.name,
        'location': booking.location.name,
        'hotel': booking.hotel.name,
        'transport': booking.transport,
        'start_date': booking.start_date,
        'end_date': booking.end_date
    }
    return JsonResponse(data)
def get_park_details(request, park_id):
    try:
        park = GamePark.objects.get(id=park_id)
        data = {
            "park_name": park.park_name,
            "location": park.location,
            "size": park.size,
            "visit_amount": park.visit_amount,
            "description": park.description,
        }
        return JsonResponse(data)
    except GamePark.DoesNotExist:
        return JsonResponse({"error": "Park not found"}, status=404)

def park(request):
    parks = GamePark.objects.all()  # Fetch all parks
    return render(request, 'myapp/park.html', {'parks': parks})
from .models import Booking, Hotel, Manager  # Make sure you have imported the models



def dashboard(request):
    manager_id = request.session.get('manager_id')  # Get the logged-in manager's ID
    if not manager_id:
        return redirect('login')  # Redirect to login if not authenticated

    try:
        manager = Manager.objects.get(id=manager_id)  # Retrieve the manager from the session
    except Manager.DoesNotExist:
        return redirect('login')  # Redirect if the manager doesn't exist (session might be invalid)

    # Fetch other data for the dashboard
    total_visitors = Booking.objects.count()
    pending_visitors = Booking.objects.filter(status='pending').count()
    approved_visitors = Booking.objects.filter(status='approved').count()
    total_hotels = Hotel.objects.count()
    total_managers = Manager.objects.count()

    context = {
        'manager': manager,  # Pass the manager object
        'total_visitors': total_visitors,
        'pending_visitors': pending_visitors,
        'approved_visitors': approved_visitors,
        'total_hotels': total_hotels,
        'total_managers': total_managers,
    }

    return render(request, 'myapp/dashboard.html', context)


def booking(request):
    bookings = Booking.objects.all()  # Fetch all bookings
    return render(request, 'myapp/booking.html', {'bookings': bookings})

def approve_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = Booking.APPROVED  # Change status to approved
    booking.save()  # Save the updated booking
    return redirect('booking')  # Redirect back to the booking list

def reject_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = Booking.REJECTED  # Change status to rejected
    booking.save()  # Save the updated booking
    return redirect('booking')  # Redirect back to the booking list
def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)  # Retrieve booking by ID
    if request.method == 'POST':
        booking.name = request.POST.get('name')
        booking.visited_place = request.POST.get('visited_place')
        booking.location = request.POST.get('location')
        booking.hotel = request.POST.get('hotel')
        booking.transport = request.POST.get('transport')
        booking.booking_date = request.POST.get('booking_date')
        booking.expired_date = request.POST.get('expired_date')
        booking.save()  # Save the updated booking
        return redirect('booking')  # Redirect to booking page after updating

    return render(request, 'myapp/edit_booking.html', {'booking': booking})

# View for deleting a booking
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)  # Retrieve booking by ID
    if request.method == 'POST':
        booking.delete()  # Delete the booking
        return redirect('booking')  # Redirect to booking page after deleting
    return render(request, 'dashboard/delete_booking.html', {'booking': booking})

def fetch_hotels(request):
    hotels = Hotel.objects.all()  # Querying all hotels from the database
    hotels_data = [{"name": hotel.name, "address": hotel.address} for hotel in hotels]
    return JsonResponse({"hotels": hotels_data})




def fetch_deals(request):
    if request.method == 'POST':
        location_id = request.POST.get('location')
        place_id = request.POST.get('place_to_visit')
        hotel_id = request.POST.get('hotel')
        start_date = request.POST.get('startDate')
        end_date = request.POST.get('endDate')
        name = request.POST.get('name')
        transport = request.POST.get('transport')
        image = request.FILES.get('image')  # Handle uploaded image

        # Check if all required fields are filled
        if location_id and place_id and hotel_id and start_date and end_date:
            try:
                location = Location.objects.get(id=location_id)
                place = PlaceToVisit.objects.get(id=place_id)
                hotel = Hotel.objects.get(id=hotel_id)

                # Save booking
                Booking.objects.create(
                    location=location,
                    place_to_visit=place,
                    hotel=hotel,
                    start_date=start_date,
                    end_date=end_date,
                    name=name,
                    transport=transport,
                    image=image
                )

                # Redirect to the index page
                return redirect('index')
            except Exception as e:
                return render(request, 'myapp/fetch_deals.html', {
                    'error': f"Error saving booking: {e}",
                    'locations': Location.objects.all()
                })

        return render(request, 'myapp/fetch_deals.html', {
            'error': "All fields are required.",
            'locations': Location.objects.all()
        })

    # For GET requests, prepare the data to populate the form
    locations = Location.objects.all()
    return render(request, 'myapp/fetch_deals.html', {'locations': locations})

def fetch_places(request, location_id):
    location = get_object_or_404(Location, id=location_id)
    places = location.places.all()
    places_data = [{"id": place.id, "name": place.name} for place in places]
    return JsonResponse({"places": places_data})


def fetch_hotels(request, place_id):
    place = get_object_or_404(PlaceToVisit, id=place_id)
    hotels = place.hotels.all()
    hotels_data = [{"id": hotel.id, "name": hotel.name} for hotel in hotels]
    return JsonResponse({"hotels": hotels_data})
def fetch_hotels(request, place_id):
    try:
        place = get_object_or_404(PlaceToVisit, id=place_id)
        hotels = place.hotels.all()
        hotels_data = [{"id": hotel.id, "name": hotel.name, "address": hotel.address} for hotel in hotels]
        return JsonResponse({"hotels": hotels_data})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)



def fetch_deals_view(request):
    locations = Location.objects.all()
    hotels = Hotel.objects.all()
    places_to_visit = PlaceToVisit.objects.all()

    return render(request, 'fetch_deals.html', {
        'locations': locations,
        'hotels': hotels,
        'places_to_visit': places_to_visit,
    })


def location_list(request):
    locations = Location.objects.all()
    return render(request, 'myapp/location_list.html', {'locations': locations})


def places_in_location(request, location_id):
    location = get_object_or_404(Location, id=location_id)
    places = location.places.all()
    return render(request, 'myapp/places_in_location.html', {'location': location, 'places': places})


def hotels_near_place(request, place_id):
    place = get_object_or_404(PlaceToVisit, id=place_id)
    hotels = place.hotels.all()
    return render(request, 'myapp/hotels_near_place.html', {'place': place, 'hotels': hotels})


def register_manager(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        telephone = request.POST.get('number')
        email = request.POST.get('email')
        location = request.POST.get('location')
        password = request.POST.get('password')
        profile_picture = request.FILES.get('profile_picture')  # For file upload

        # Check if the email already exists in the database
        if Manager.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered.')
            return redirect('register_manager')

        # Create a new manager if the email is unique
        Manager.objects.create(
            name=name,
            telephone=telephone,
            email=email,
            location=location,
            password=password,
            profile_picture=profile_picture  # Save the uploaded image
        )
        return redirect('login')

    return render(request, 'myapp/register.html')

def more(request, park_id=None):
    if park_id:
        park = get_object_or_404(GamePark, id=park_id)
    else:
        park = GamePark.objects.first()

    images = [
        getattr(park, f'image_{i}')
        for i in range(1, 6)
        if getattr(park, f'image_{i}', None) and getattr(park, f'image_{i}').name
    ]

    related_parks = GamePark.objects.all()[:6]

    return render(request, 'myapp/more.html', {
        'park': park,
        'images': images,
        'related_parks': related_parks,
    })


def contact(request):
    return render(request, 'myapp/contact.html')


def register(request):
    return render(request, 'myapp/register.html')


def hello(request):
    return render(request, 'myapp/hello.html')


def login(request):
    return render(request, 'myapp/login.html')
def hy(request):
    return render(request, 'myapp/hy.html')


def index(request):
    parks = GamePark.objects.all()[:4]
    allpark = GamePark.objects.all()
    return render(request, 'myapp/index.html', {'parks': parks, 'allpark': allpark})


def about(request):
    return render(request, 'myapp/about.html')


def fetch(request):
    return render(request, 'myapp/fetch.html')


def deals(request):
    deals = SearchDeal.objects.all()
    return render(request, 'myapp/deals.html', {'deals': deals})


def submit_deal(request):
    if request.method == 'POST':
        destination = request.POST.get('Location')
        price = request.POST.get('Price')
        hotel = request.POST.get('Hotel')
        start_date = request.POST.get('startDate')
        end_date = request.POST.get('endDate')

        SearchDeal.objects.create(
            destination=destination,
            price=price,
            hotel=hotel,
            start_date=start_date,
            end_date=end_date
        )
        return redirect('deals')

    return render(request, 'myapp/deals.html')
