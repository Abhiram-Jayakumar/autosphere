from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.utils.timezone import now
from Customer.models import Customer, RentalBooking, TestDriveBooking, Vehicle, VehicleFeatures
from Dealer.models import Dealer
from Showroom.models import Showroom
from django.db.models import Sum, Count, Q

def showroom_registration(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        id_proof_number = request.POST.get('id_proof_number')
        address = request.POST.get('address')
        profile_image_showroom = request.FILES.get('profile_image_showroom')
        
        showroom = Showroom(
            name=name,
            email=email,
            phone=phone,
            password=password,  
            id_proof_number=id_proof_number,
            address=address,
            profile_image_showroom=profile_image_showroom,
            registered_at=now(),
            approval_status=False
        )
        showroom.save()
        return redirect("Customer:index")
    
    return render(request, 'Showroom/Showroom_registration.html')

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////

def Showroom_home(request):
    return render(request,'Showroom/Showroom_home.html')

#/////////////////////////////////////////////////////////////////////////////////////////

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

        print(f"🛠 DEBUG: Session Values - Dealer ID: {dealer_id}, Showroom Dealer ID: {showroom_id}, Customer ID: {customer_id}")

        vehicle = None  

        if showroom_id:
            print("🛠 DEBUG: Showroom Dealer is adding the vehicle")
            showroom = Showroom.objects.filter(id=showroom_id).first()
            if not showroom:
                return render(request, "Showroom/add_vehicle.html", {"message": "Showroom dealer not found!"})

            vehicle = Vehicle(
                showroom_dealer=showroom,  
                dealer=None,  
                owner=None,  
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

        elif dealer_id:  
            print("🛠 DEBUG: Dealer is adding the vehicle")
            dealer = Dealer.objects.filter(id=dealer_id).first()
            if not dealer:
                return render(request, "Showroom/add_vehicle.html", {"message": "Dealer not found!"})

            vehicle = Vehicle(
                dealer=dealer,
                showroom_dealer=None,  
                owner=None,  
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
            print("🛠 DEBUG: Customer is adding the vehicle")
            customer = Customer.objects.filter(id=customer_id).first()
            if not customer:
                return render(request, "Showroom/add_vehicle.html", {"message": "Customer not found!"})

            vehicle = Vehicle(
                owner=customer, 
                dealer=None,  
                showroom_dealer=None,  
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
            print("🛠 DEBUG: Unauthorized user tried adding a vehicle")
            return render(request, "Showroom/add_vehicle.html", {"message": "Unauthorized! You must be logged in to add a vehicle."})

        vehicle.save()
        print(f"✅ Vehicle added successfully! ID: {vehicle.id}, Dealer: {vehicle.dealer}, Showroom Dealer: {vehicle.showroom_dealer}")

        return redirect('Showroom:Showroom_home')

    return render(request, "Showroom/add_vehicle.html")


#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


def showroom_vehicles(request):
    showroom_id = request.session.get('sid')  

    if not showroom_id:
        return redirect("Showroom:login")  

    showroom = get_object_or_404(Showroom, id=showroom_id)
    vehicles = Vehicle.objects.filter(showroom_dealer=showroom) 

    return render(request, "Showroom/showroom_vehicles.html", {"vehicles": vehicles})


#///////////////////////////////////////////////////////////////////////////////////////////////////////////////

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

        return redirect('Showroom:showroom_vehicles')  

    return render(request, "Showroom/add_vehicle_features.html", {"vehicle": vehicle})


#///////////////////////////////////////////////////////////////////////////////////////////////////////////////


def showroom_bookings(request):
    if "sid" not in request.session:
        return redirect("Showroom:login") 

    showroom_id = request.session["sid"]

    test_drives = TestDriveBooking.objects.filter(vehicle__showroom_dealer_id=showroom_id).order_by("-date", "-time")
    rentals = RentalBooking.objects.filter(vehicle__showroom_dealer_id=showroom_id).order_by("-rental_date")

    return render(
        request,
        "Showroom/showroom_bookings.html",
        {"test_drives": test_drives, "rentals": rentals},
    )


#//////////////////////////////////////////////////////////////////////////////////////////////////////////////


def approve_booking(request, booking_type, booking_id):
    if booking_type == "test_drive":
        booking = get_object_or_404(TestDriveBooking, id=booking_id)
    elif booking_type == "rental":
        booking = get_object_or_404(RentalBooking, id=booking_id)
    else:
        return redirect("Showroom:showroom_bookings")

    booking.status = "Accepted"
    booking.save()
    messages.success(request, "Booking approved successfully!")
    return redirect("Showroom:showroom_bookings")

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////


def reject_booking(request, booking_type, booking_id):
    if booking_type == "test_drive":
        booking = get_object_or_404(TestDriveBooking, id=booking_id)
    elif booking_type == "rental":
        booking = get_object_or_404(RentalBooking, id=booking_id)
    else:
        return redirect("Showroom:showroom_bookings")

    booking.status = "Rejected"
    booking.save()
    messages.error(request, "Booking rejected.")
    return redirect("Showroom:showroom_bookings")

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////


def mark_contacted(request, booking_id):
    booking = get_object_or_404(TestDriveBooking, id=booking_id)

    if request.session.get("sid") != booking.vehicle.showroom_dealer.id:
        return redirect("Showroom:showroom_bookings")  

    booking.Contancted = "Contacted"
    booking.save()
    messages.success(request, "Marked as contacted.")
    return redirect("Showroom:showroom_bookings")

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////


def edit_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)

    if request.method == "POST":
        vehicle.title = request.POST["title"]
        vehicle.brand = request.POST["brand"]
        vehicle.model = request.POST["model"]
        vehicle.year = request.POST["year"]
        vehicle.price = request.POST["price"]
        vehicle.vehicle_type = request.POST["vehicle_type"]
        vehicle.mileage = request.POST.get("mileage", None)
        vehicle.fuel_type = request.POST["fuel_type"]

        if "image" in request.FILES:
            vehicle.image = request.FILES["image"]

        vehicle.save()
        messages.success(request, "Vehicle details updated successfully!")
        return redirect("Showroom:showroom_vehicles")

    return render(request, "Showroom/edit_vehicle.html", {"vehicle": vehicle})

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////

def showroom_profile(request):
    showroom_id = request.session.get('sid')
    if not showroom_id:
        return redirect("Showroom:login")
    
    showroom = get_object_or_404(Showroom, id=showroom_id)
    return render(request, "Showroom/showroom_profile.html", {"showroom": showroom})

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////


def edit_showroom_profile(request):
    showroom_id = request.session.get('sid')
    showroom = get_object_or_404(Showroom, id=showroom_id)

    if request.method == "POST":
        showroom.name = request.POST["name"]
        showroom.email = request.POST["email"]
        showroom.phone = request.POST["phone"]
        showroom.address = request.POST["address"]

        if "profile_image" in request.FILES:
            showroom.profile_image_showroom = request.FILES["profile_image"]

        showroom.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("Showroom:showroom_profile")

    return render(request, "Showroom/edit_showroom_profile.html", {"showroom": showroom})

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////


def change_showroom_password(request):
    showroom_id = request.session.get('sid')
    showroom = get_object_or_404(Showroom, id=showroom_id)

    if request.method == "POST":
        current_password = request.POST["current_password"]
        new_password = request.POST["new_password"]
        confirm_password = request.POST["confirm_password"]

        if showroom.password != current_password:
            messages.error(request, "Incorrect current password!")
        elif new_password != confirm_password:
            messages.error(request, "Passwords do not match!")
        else:
            showroom.password = new_password
            showroom.save()
            messages.success(request, "Password changed successfully!")
            return redirect("Showroom:showroom_profile")

    return render(request, "Showroom/change_showroom_password.html")


#////////////////////////////////////////////////////////////////////////////////////////////////////////////


def showroom_dashboard(request):
    showroom_id = request.session.get("sid")  

    if not showroom_id:
        return render(request, "Showroom/error.html", {"message": "Showroom ID not found in session"})

    try:
        showroom = Showroom.objects.get(id=showroom_id) 
    except Showroom.DoesNotExist:
        return render(request, "Showroom/error.html", {"message": "Invalid Showroom ID"})

    total_vehicles_added = Vehicle.objects.filter(showroom_dealer=showroom).count()

    total_vehicles_for_sale = Vehicle.objects.filter(showroom_dealer=showroom, vehicle_type="sale").count()
    total_vehicles_for_rent = Vehicle.objects.filter(showroom_dealer=showroom, vehicle_type="rent").count()

    total_test_drive_bookings = TestDriveBooking.objects.filter(vehicle__showroom_dealer=showroom).count()
    sold_vehicles = TestDriveBooking.objects.filter(vehicle__showroom_dealer=showroom, status="Accepted").count()
    total_test_drive_earnings = TestDriveBooking.objects.filter(
        vehicle__showroom_dealer=showroom, payment_status="Paid"
    ).aggregate(Sum("Payment_amount"))["Payment_amount__sum"] or 0

    total_rental_bookings = RentalBooking.objects.filter(vehicle__showroom_dealer=showroom).count()
    total_rented_vehicles = RentalBooking.objects.filter(vehicle__showroom_dealer=showroom, status="Accepted").count()
    total_rental_earnings = RentalBooking.objects.filter(
        vehicle__showroom_dealer=showroom, payment_status="Paid"
    ).aggregate(Sum("vehicle__price"))["vehicle__price__sum"] or 0

    vehicles = Vehicle.objects.filter(showroom_dealer=showroom)
    total_value_of_added_vehicles = sum(
        (vehicle.price * 100000) if vehicle.vehicle_type == "sale" else vehicle.price
        for vehicle in vehicles
    )

    total_profit = total_test_drive_earnings + total_rental_earnings  
    context = {
        "total_vehicles_added": total_vehicles_added,
        "total_vehicles_for_sale": total_vehicles_for_sale,
        "total_vehicles_for_rent": total_vehicles_for_rent,
        "total_test_drive_bookings": total_test_drive_bookings,
        "sold_vehicles": sold_vehicles,
        "total_test_drive_earnings": total_test_drive_earnings,
        "total_rental_bookings": total_rental_bookings,
        "total_rented_vehicles": total_rented_vehicles,
        "total_rental_earnings": total_rental_earnings,
        "total_value_of_added_vehicles": total_value_of_added_vehicles,
        "total_profit": total_profit,
    }

    return render(request, "Showroom/showroom_dashboard.html", context)