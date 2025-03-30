# Create your views here.
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.utils.timezone import now
from decimal import Decimal
from Customer.models import Customer, RentalBooking, TestDriveBooking, Vehicle, VehicleFeatures
from Dealer.models import Dealer
from Showroom.models import Showroom
from django.db.models import Sum



def dealer_registration(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        id_proof_number = request.POST.get('id_proof_number')
        address = request.POST.get('address')
        profile_image_dealer = request.FILES.get('profile_image_dealer')
        
        dealer = Dealer(
            name=name,
            email=email,
            phone=phone,
            password=password, 
            id_proof_number=id_proof_number,
            address=address,
            profile_image_dealer=profile_image_dealer,
            registered_at=now(),
            approval_status=False
        )
        dealer.save()
        return redirect("Customer:index")

    return render(request, 'Dealer/Dealer_registration.html')

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////

def Dealer_home(request):
    return render(request,'Dealer/Dealer_home.html')

#///////////////////////////////////////////////////////////////////////////////////


def add_vehicle(request):
    if request.method == "POST":
        title = request.POST.get('title')
        brand = request.POST.get('brand')
        model = request.POST.get('model')
        year = request.POST.get('year')
        price = request.POST.get('price')
        vehicle_type = request.POST.get('vehicle_type')
        description = request.POST.get('description')
        mileage = request.POST.get('mileage', None)
        fuel_type = request.POST.get('fuel_type')
        transmission = request.POST.get('transmission')
        image = request.FILES.get('image')
        dealer_id = request.session.get('did')
        showroom_id = request.session.get('sid')
        customer_id = request.session.get('cid') 

        print(f"Session Values - Dealer ID: {dealer_id}, Showroom Dealer ID: {showroom_id}, Customer ID: {customer_id}")

        if dealer_id:
            dealer = Dealer.objects.filter(id=dealer_id).first()
            if not dealer:
                return render(request, "Dealer/add_vehicle.html", {"message": "Dealer not found!"})

            vehicle = Vehicle(
                dealer=dealer,
                title=title,
                brand=brand,
                model=model,
                year=int(year),
                price=float(price),
                vehicle_type=vehicle_type,
                description=description,
                mileage=int(mileage) if mileage else None,
                fuel_type=fuel_type,
                transmission=transmission,
                image=image,
                created_at=now(),
            )

        elif showroom_id:
            showroom = Showroom.objects.filter(id=showroom_id).first()
            if not showroom:
                return render(request, "Dealer/add_vehicle.html", {"message": "Showroom dealer not found!"})

            vehicle = Vehicle(
                showroom_dealer=showroom,
                title=title,
                brand=brand,
                model=model,
                year=int(year),
                price=float(price),
                vehicle_type=vehicle_type,
                description=description,
                mileage=int(mileage) if mileage else None,
                fuel_type=fuel_type,
                transmission=transmission,
                image=image,
                created_at=now(),
            )

        elif customer_id:  
            customer = Customer.objects.filter(id=customer_id).first()
            if not customer:
                return render(request, "Dealer/add_vehicle.html", {"message": "Customer not found!"})

            vehicle = Vehicle(
                owner=customer,  
                title=title,
                brand=brand,
                model=model,
                year=int(year),
                price=float(price),
                vehicle_type=vehicle_type,
                description=description,
                mileage=int(mileage) if mileage else None,
                fuel_type=fuel_type,
                transmission=transmission,
                image=image,
                created_at=now(),
            )

        else:
            return render(request, "Dealer/add_vehicle.html", {"message": "Unauthorized! You must be logged in to add a vehicle."})

        vehicle.save()
        print("✅ Vehicle added successfully!")
        return redirect('Dealer:Dealer_home')

    return render(request, "Dealer/add_vehicle.html")


#//////////////////////////////////////////////////////////////////////////////////////////////

def dealer_vehicles(request):
    dealer_id = request.session.get('did')  

    if not dealer_id:
        return redirect('Dealer:dealer_login') 

    vehicles = Vehicle.objects.filter(dealer_id=dealer_id)  

    return render(request, "Dealer/dealer_vehicles.html", {"vehicles": vehicles})

#//////////////////////////////////////////////////////////////////////////////////////////////

def add_vehicle_features(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)

    if request.method == "POST":
        previous_owners = request.POST.get('previous_owners', 1)
        condition = request.POST.get('condition', "Used")
        color = request.POST.get('color', "Unknown")
        seating_capacity = request.POST.get('seating_capacity', 4) 
        engine_capacity = request.POST.get('engine_capacity', "")
        fuel_tank_capacity = request.POST.get('fuel_tank_capacity', None)
        features = request.POST.get('features', "")
        safety_rating = request.POST.get('safety_rating', None)
        gps_enabled = request.POST.get('gps_enabled') == "on"
        bluetooth_connectivity = request.POST.get('bluetooth_connectivity') == "on"
        negotiable = request.POST.get('negotiable') == "on"
        insurance_valid_till = request.POST.get('insurance_valid_till') if request.POST.get('insurance_valid_till') else None
        warranty_available = request.POST.get('warranty_available') == "on"

        vehicle_features, created = VehicleFeatures.objects.get_or_create(
            vehicle=vehicle,
            defaults={ 
                "previous_owners": int(previous_owners),
                "condition": condition,
                "color": color,
                "seating_capacity": int(seating_capacity),
                "engine_capacity": engine_capacity,
                "fuel_tank_capacity": int(fuel_tank_capacity) if fuel_tank_capacity else None,
                "features": features,
                "safety_rating": float(safety_rating) if safety_rating else None,
                "gps_enabled": gps_enabled,
                "bluetooth_connectivity": bluetooth_connectivity,
                "negotiable": negotiable,
                "insurance_valid_till": insurance_valid_till,
                "warranty_available": warranty_available,
            }
        )

        if not created:
            vehicle_features.previous_owners = int(previous_owners)
            vehicle_features.condition = condition
            vehicle_features.color = color
            vehicle_features.seating_capacity = int(seating_capacity)
            vehicle_features.engine_capacity = engine_capacity
            vehicle_features.fuel_tank_capacity = int(fuel_tank_capacity) if fuel_tank_capacity else None
            vehicle_features.features = features
            vehicle_features.safety_rating = float(safety_rating) if safety_rating else None
            vehicle_features.gps_enabled = gps_enabled
            vehicle_features.bluetooth_connectivity = bluetooth_connectivity
            vehicle_features.negotiable = negotiable
            vehicle_features.insurance_valid_till = insurance_valid_till
            vehicle_features.warranty_available = warranty_available
            vehicle_features.save() 

        return redirect('Dealer:dealer_vehicles') 

    return render(request, "Dealer/add_vehicle_features.html", {"vehicle": vehicle})

#///////////////////////////////////////////////////////////////////////////////////////////

def dealer_bookings(request):
    if "did" not in request.session:
        return redirect("Dealer:login")  
    dealer_id = request.session["did"]

    test_drives = TestDriveBooking.objects.filter(vehicle__dealer_id=dealer_id).order_by("-date", "-time")
    rentals = RentalBooking.objects.filter(vehicle__dealer_id=dealer_id).order_by("-rental_date")

    return render(
        request,
        "Dealer/dealer_bookings.html",
        {"test_drives": test_drives, "rentals": rentals},
    )

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////


def approve_dealer_booking(request, booking_type, booking_id):
    if booking_type == "test_drive":
        booking = get_object_or_404(TestDriveBooking, id=booking_id)
    elif booking_type == "rental":
        booking = get_object_or_404(RentalBooking, id=booking_id)
    else:
        return redirect("Dealer:dealer_bookings")

    booking.status = "Accepted"
    booking.save()
    messages.success(request, "Booking approved successfully!")
    return redirect("Dealer:dealer_bookings")

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////


def reject_dealer_booking(request, booking_type, booking_id):
    if booking_type == "test_drive":
        booking = get_object_or_404(TestDriveBooking, id=booking_id)
    elif booking_type == "rental":
        booking = get_object_or_404(RentalBooking, id=booking_id)
    else:
        return redirect("Dealer:dealer_bookings")

    booking.status = "Rejected"
    booking.save()
    messages.error(request, "Booking rejected.")
    return redirect("Dealer:dealer_bookings")

#///////////////////////////////////////////////////////////////////////////////////////////

def dealer_vehicle_list(request):
    if "did" not in request.session:
        return redirect("Dealer:login")  
    vehicles = Vehicle.objects.filter(vehicle_type=Vehicle.SALE) 
    return render(request, "Dealer/dealer_vehicle_list.html", {"vehicles": vehicles})

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////


def dealer_vehicle_detail(request, vehicle_id):
    if "did" not in request.session:
        return redirect("Dealer:login") 

    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    return render(request, "Dealer/dealer_vehicle_detail.html", {"vehicle": vehicle})

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////


def book_test_drive_for_dealer(request, vehicle_id):
    if "did" not in request.session:  
        messages.error(request, "You must be logged in to book a test drive.")
        return redirect("Customer:Login")  

    vehicle = get_object_or_404(Vehicle, id=vehicle_id)

    if request.method == "POST":
        test_drive_date = request.POST.get("date")
        test_drive_time = request.POST.get("time")

        if not test_drive_date or not test_drive_time:
            messages.error(request, "Please select both date and time.")
            return redirect("Dealer:dealer_vehicle_detail", vehicle_id=vehicle.id)

        dealer = get_object_or_404(Dealer, id=request.session["did"])

        TestDriveBooking.objects.create(
            dealer=dealer,  
            vehicle=vehicle,
            date=test_drive_date,
            time=test_drive_time,
            status="Pending",
            payment_status="Pending",
        )

        messages.success(request, "Test drive booked successfully!")
        return redirect("Dealer:dealer_vehicle_list")  

    return render(request, "Dealer/book_test_drive.html", {"vehicle": vehicle})
    
#///////////////////////////////////////////////////////////////////////////////////////////

def Dealer_booked_vehicel(request):
    if "did" not in request.session:
        return redirect("Customer:Login") 
    
    dealer_id = request.session["did"] 
    test_drive_bookings = TestDriveBooking.objects.filter(dealer_id=dealer_id).select_related("vehicle")

    return render(request, "Dealer/Dealer_booked_vehicel.html", {"test_drive_bookings": test_drive_bookings})

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////


def mark_interested_dealer(request, booking_id):
    booking = get_object_or_404(TestDriveBooking, id=booking_id)

    if request.session.get("did") != booking.dealer.id:
        messages.error(request, "Unauthorized action.")
        return redirect("Dealer:Dealer_booked_vehicel")

    booking.Intrested = "Intrested"
    booking.save()
    messages.success(request, "Marked as Interested!")
    return redirect("Dealer:Dealer_booked_vehicel")

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////


def mark_not_interested_dealer(request, booking_id):
    booking = get_object_or_404(TestDriveBooking, id=booking_id)

    if request.session.get("did") != booking.dealer.id:
        messages.error(request, "Unauthorized action.")
        return redirect("Dealer:Dealer_booked_vehicel")

    booking.Intrested = "Not-Intrested"
    booking.save()
    messages.error(request, "Marked as Not Interested.")
    return redirect("Dealer:Dealer_booked_vehicel")

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////


def make_payment_dealer(request, booking_id):
    booking = get_object_or_404(TestDriveBooking, id=booking_id)

    vehicle_price = booking.vehicle.price * Decimal(100000)  

    advance_amount = vehicle_price * Decimal(0.1) 

    if request.method == "POST":
        booking.payment_status = "Paid"
        booking.Payment_amount = advance_amount  
        booking.save()
        messages.success(request, f"Payment of ₹{advance_amount} successful!")
        return redirect("Dealer:Dealer_booked_vehicel")

    return render(
        request,
        "Dealer/make_payment.html",
        {
            "booking": booking,
            "vehicle_price_lakh": booking.vehicle.price,  
            "advance_amount": advance_amount, 
        },
    )
   

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////
 
def mark_as_contacted(request, booking_id):
    booking = get_object_or_404(TestDriveBooking, id=booking_id)
    
    booking.Contancted = "Contacted"
    booking.save()
    
    messages.success(request, "Marked as Contacted!")
    return redirect("Dealer:dealer_bookings") 

#///////////////////////////////////////////////////////////////////////////////////////////

def edit_dealer_vehicle(request, vehicle_id):
    if "did" not in request.session:
        return redirect("Dealer:dealer_login")

    vehicle = get_object_or_404(Vehicle, id=vehicle_id, dealer_id=request.session["did"])

    if request.method == "POST":
        vehicle.title = request.POST["title"]
        vehicle.brand = request.POST["brand"]
        vehicle.model = request.POST["model"]
        vehicle.year = request.POST["year"]
        vehicle.price = request.POST["price"]
        vehicle.fuel_type = request.POST["fuel_type"]
        vehicle.transmission = request.POST["transmission"]
        vehicle.vehicle_type = request.POST["vehicle_type"]

        if "image" in request.FILES:
            vehicle.image = request.FILES["image"]

        vehicle.save()
        return redirect("Dealer:dealer_vehicles")

    return render(request, "Dealer/edit_dealer_vehicle.html", {"vehicle": vehicle})

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def dealer_profile(request):
    dealer_id = request.session.get('did')  

    if not dealer_id:
        return redirect('Dealer:dealer_login') 
    dealer = get_object_or_404(Dealer, id=dealer_id)
    return render(request, "Dealer/dealer_profile.html", {"dealer": dealer})

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////

def edit_dealer_details(request):
    dealer_id = request.session.get('did')

    if not dealer_id:
        return redirect('Dealer:dealer_login')

    dealer = get_object_or_404(Dealer, id=dealer_id)

    if request.method == "POST":
        dealer.name = request.POST["name"]
        dealer.phone = request.POST["phone"]
        dealer.address = request.POST["address"]

        if "profile_image_dealer" in request.FILES:
            dealer.profile_image_dealer = request.FILES["profile_image_dealer"]

        dealer.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("Dealer:dealer_profile")

    return render(request, "Dealer/edit_dealer_details.html", {"dealer": dealer})

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////

def change_dealer_password(request):
    dealer_id = request.session.get('did')

    if not dealer_id:
        return redirect('Dealer:dealer_login')

    dealer = get_object_or_404(Dealer, id=dealer_id)

    if request.method == "POST":
        old_password = request.POST["old_password"]
        new_password = request.POST["new_password"]
        confirm_password = request.POST["confirm_password"]

        if old_password != dealer.password:
            messages.error(request, "Old password is incorrect!")
            return redirect("Dealer:change_dealer_password")

        if new_password != confirm_password:
            messages.error(request, "New passwords do not match!")
            return redirect("Dealer:change_dealer_password")

        dealer.password = new_password  
        dealer.save()
        messages.success(request, "Password changed successfully!")
        return redirect("Dealer:dealer_profile")

    return render(request, "Dealer/change_dealer_password.html")

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def dealer_dashboard(request):
    dealer_id = request.session.get("did")  

    if not dealer_id:
        return render(request, "Dealer/error.html", {"message": "Dealer ID not found in session"})

    try:
        dealer = Dealer.objects.get(id=dealer_id)  
    except Dealer.DoesNotExist:
        return render(request, "Dealer/error.html", {"message": "Invalid Dealer ID"})

    total_vehicles_added = Vehicle.objects.filter(dealer=dealer).count()

    total_vehicles_for_sale = Vehicle.objects.filter(dealer=dealer, vehicle_type="sale").count()
    total_vehicles_for_rent = Vehicle.objects.filter(dealer=dealer, vehicle_type="rent").count()

    total_test_drive_bookings = TestDriveBooking.objects.filter(vehicle__dealer=dealer).count()
    sold_vehicles = TestDriveBooking.objects.filter(vehicle__dealer=dealer, status="Accepted").count()
    total_sales_earnings = TestDriveBooking.objects.filter(
        vehicle__dealer=dealer, payment_status="Paid"
    ).aggregate(Sum("Payment_amount"))["Payment_amount__sum"] or 0

    total_rental_bookings = RentalBooking.objects.filter(vehicle__dealer=dealer).count()
    total_rented_vehicles = RentalBooking.objects.filter(vehicle__dealer=dealer, status="Accepted").count()
    total_rental_earnings = RentalBooking.objects.filter(
        vehicle__dealer=dealer, payment_status="Paid"
    ).aggregate(Sum("vehicle__price"))["vehicle__price__sum"] or 0

    vehicles = Vehicle.objects.filter(dealer=dealer)
    total_value_of_added_vehicles = sum(
        (vehicle.price * 100000) if vehicle.vehicle_type == "sale" else vehicle.price
        for vehicle in vehicles
    )
    total_profit = total_sales_earnings + total_rental_earnings  

    context = {
        "total_vehicles_added": total_vehicles_added,
        "total_vehicles_for_sale": total_vehicles_for_sale,
        "total_vehicles_for_rent": total_vehicles_for_rent,
        "total_test_drive_bookings": total_test_drive_bookings,
        "sold_vehicles": sold_vehicles,
        "total_sales_earnings": total_sales_earnings,
        "total_rental_bookings": total_rental_bookings,
        "total_rented_vehicles": total_rented_vehicles,
        "total_rental_earnings": total_rental_earnings,
        "total_value_of_added_vehicles": total_value_of_added_vehicles,
        "total_profit": total_profit,
    }

    return render(request, "Dealer/dealer_dashboard.html", context)