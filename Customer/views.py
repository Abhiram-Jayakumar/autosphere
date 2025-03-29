from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now
from django.contrib import messages
from Admin.models import Admin
from Customer.models import Customer, RentalBooking, TestDriveBooking, Vehicle, VehicleFeatures
from Dealer.models import Dealer
from Showroom.models import Showroom
from decimal import Decimal
# Create your views here.

def index(request):
    return render(request,'Customer/index.html')

#////////////////////////////////////////////////////////////////////////////////////     


def registartion(request):
    return render(request,'Customer/registration.html')


def customer_registration(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        id_proof_number = request.POST.get('id_proof_number')
        address = request.POST.get('address')
        profile_image = request.FILES.get('profile_image')
        
        customer = Customer(
            name=name,
            email=email,
            phone=phone,
            password=password,  # Not hashed as requested
            id_proof_number=id_proof_number,
            address=address,
            profile_image=profile_image,
            registered_at=now(),
            approval_status=False
        )
        customer.save()
        return redirect("Customer:index")
    
    return render(request, 'Customer/customer_register.html')

##########################Login############

def login(request):
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        Clogin=Customer.objects.filter(email=email,password=password,approval_status=True).count()
        Dlogin=Dealer.objects.filter(email=email,password=password,approval_status=True).count()
        Alogin=Admin.objects.filter(email=email,password=password).count()
        Slogin=Showroom.objects.filter(email=email,password=password,approval_status=True).count()
        if Clogin > 0:
            Cadmin=Customer.objects.get(email=email,password=password,approval_status=1)
            request.session['cid']=Cadmin.id
            return redirect('Customer:Customer_home')
        elif Dlogin > 0:
            Dadmin=Dealer.objects.get(email=email,password=password,approval_status=1)
            request.session['did']=Dadmin.id
            return redirect('Dealer:Dealer_home')
        elif Alogin > 0:
            Aadmin=Admin.objects.get(email=email,password=password)
            request.session['aid']=Aadmin.id
            return redirect('Admin:Admin_home')
        elif Slogin > 0:
            Sadmin=Showroom.objects.get(email=email,password=password,approval_status=1)
            request.session['sid']=Sadmin.id
            return redirect('Showroom:Showroom_home')
        
        else:
            error="Invalid Credentials!!"
            return render(request,"Customer/Login.html",{'ERR':error})
    else:
        return render(request, "Customer/Login.html")
    
    #####customer home#######
    
def Customer_home(request):
    return render(request,'Customer/Customer_home.html')

#///////////////////////////////////////////////////////////////////////////////////////////////////////////


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

        # Retrieve session user ID
        dealer_id = request.session.get('did')
        showroom_id = request.session.get('sid')
        customer_id = request.session.get('cid')  # NEW: Get Customer ID

        print(f"Session Values - Dealer ID: {dealer_id}, Showroom Dealer ID: {showroom_id}, Customer ID: {customer_id}")

        if dealer_id:
            dealer = Dealer.objects.filter(id=dealer_id).first()
            if not dealer:
                return render(request, "Customer/add_vehicle.html", {"message": "Dealer not found!"})

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
                return render(request, "Customer/add_vehicle.html", {"message": "Showroom dealer not found!"})

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

        elif customer_id:  # NEW: Allow Customers to Add Vehicles
            customer = Customer.objects.filter(id=customer_id).first()
            if not customer:
                return render(request, "Customer/add_vehicle.html", {"message": "Customer not found!"})

            vehicle = Vehicle(
                owner=customer,  # Assign to Customer
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
            return render(request, "Customer/add_vehicle.html", {"message": "Unauthorized! You must be logged in to add a vehicle."})

        vehicle.save()
        print("✅ Vehicle added successfully!")
        return redirect('Customer:Customer_home')

    return render(request, "Customer/add_vehicle.html")

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def customer_vehicles(request):
    customer_id = request.session.get('cid')  # Get logged-in customer's ID

    if not customer_id:
        return redirect('Customer:customer_login')  # Redirect to login if not authenticated

    vehicles = Vehicle.objects.filter(owner_id=customer_id)  # Get vehicles added by the customer

    return render(request, "Customer/customer_vehicles.html", {"vehicles": vehicles})

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def add_vehicle_features(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)

    if request.method == "POST":
        previous_owners = request.POST.get('previous_owners')
        condition = request.POST.get('condition')
        color = request.POST.get('color')
        seating_capacity = request.POST.get('seating_capacity')
        engine_capacity = request.POST.get('engine_capacity')
        fuel_tank_capacity = request.POST.get('fuel_tank_capacity')
        features = request.POST.get('features')  # User inputs comma-separated features
        safety_rating = request.POST.get('safety_rating')
        gps_enabled = bool(request.POST.get('gps_enabled'))
        bluetooth_connectivity = bool(request.POST.get('bluetooth_connectivity'))
        negotiable = bool(request.POST.get('negotiable'))
        insurance_valid_till = request.POST.get('insurance_valid_till')
        warranty_available = bool(request.POST.get('warranty_available'))

        VehicleFeatures.objects.create(
            vehicle=vehicle,
            previous_owners=previous_owners,
            condition=condition,
            color=color,
            seating_capacity=seating_capacity,
            engine_capacity=engine_capacity,
            fuel_tank_capacity=fuel_tank_capacity,
            features=features,
            safety_rating=safety_rating,
            gps_enabled=gps_enabled,
            bluetooth_connectivity=bluetooth_connectivity,
            negotiable=negotiable,
            insurance_valid_till=insurance_valid_till,
            warranty_available=warranty_available,
        )

        return redirect('Customer:Customer_home')  # Redirect back to listing

    return render(request, "Customer/add_vehicle_features.html", {"vehicle": vehicle})


#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def view_vehicles(request):
    vehicle_type = request.GET.get('type', 'sale')  # Default to sale
    vehicles = Vehicle.objects.filter(vehicle_type=vehicle_type)
    return render(request, "Customer/view_vehicles.html", {"vehicles": vehicles, "vehicle_type": vehicle_type})


#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def vehicle_detail(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    features = VehicleFeatures.objects.filter(vehicle=vehicle).first()  # Fetch vehicle features if available

    # Fetch rental feedbacks and include related customer name
    rental_feedbacks = RentalBooking.objects.filter(vehicle=vehicle, feedback__isnull=False).select_related('customer')

    return render(
        request, 
        "Customer/vehicle_detail.html", 
        {"vehicle": vehicle, "features": features, "rental_feedbacks": rental_feedbacks}
    )

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////


def book_test_drive(request, vehicle_id):
    if "cid" not in request.session:
        return redirect("Customer:Login")  

    customer_id = request.session["cid"]
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)

    if request.method == "POST":
        date = request.POST.get("date")
        time = request.POST.get("time")

        TestDriveBooking.objects.create(
            customer_id=customer_id,
            vehicle=vehicle,
            date=date,
            time=time,
            status="Pending",
            payment_status="Pending"
        )
        return redirect("Customer:customer_bookings")

    return render(request, "Customer/book_test_drive.html", {"vehicle": vehicle})

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def book_rental(request, vehicle_id):
    if "cid" not in request.session:
        return redirect("Customer:Login")  

    customer_id = request.session["cid"]
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)

    if request.method == "POST":
        rental_date = request.POST.get("rental_date")
        return_date = request.POST.get("return_date")
        accessories_needed = request.POST.get("accessories_needed", "")

        RentalBooking.objects.create(
            customer_id=customer_id,
            vehicle=vehicle,
            rental_date=rental_date,
            return_date=return_date,
            accessories_needed=accessories_needed,
            status="Pending",
            payment_status="Pending"
        )
        return redirect("Customer:customer_bookings")

    return render(request, "Customer/book_rental.html", {"vehicle": vehicle})

#///////////////////////////////////////////////////////////////////////////////////////////////////////////

def customer_bookings(request):
    if "cid" not in request.session:
        return redirect("Customer:Login")  # Redirect if not logged in

    customer_id = request.session["cid"]

    test_drives = TestDriveBooking.objects.filter(customer_id=customer_id).order_by("-date", "-time")
    rentals = RentalBooking.objects.filter(customer_id=customer_id).order_by("-rental_date")

    return render(
        request,
        "Customer/customer_bookings.html",
        {"test_drives": test_drives, "rentals": rentals},
    )
    
#///////////////////////////////////////////////////////////////////////////////////////////////////////////

def customer_vehicle_bookings(request):
    """Show all test drive bookings for vehicles added by the customer."""
    if "cid" not in request.session:
        return redirect("Customer:Login")  # Redirect if not logged in

    customer_id = request.session["cid"]

    # Fetch test drive bookings for customer's vehicles
    test_drives = TestDriveBooking.objects.filter(vehicle__owner_id=customer_id).order_by("-date", "-time")

    return render(
        request,
        "Customer/customer_vehicle_bookings.html",
        {"test_drives": test_drives},
    )


def approve_customer_booking(request, booking_id):
    """Approve a test drive booking for a vehicle owned by the customer."""
    booking = get_object_or_404(TestDriveBooking, id=booking_id)
    
    # Ensure the customer is the vehicle owner
    if request.session.get("cid") != booking.vehicle.owner.id:
        return redirect("Customer:customer_vehicle_bookings")

    booking.status = "Accepted"
    booking.save()
    messages.success(request, "Booking approved successfully!")
    return redirect("Customer:customer_vehicle_bookings")


def reject_customer_booking(request, booking_id):
    """Reject a test drive booking for a vehicle owned by the customer."""
    booking = get_object_or_404(TestDriveBooking, id=booking_id)
    
    # Ensure the customer is the vehicle owner
    if request.session.get("cid") != booking.vehicle.owner.id:
        return redirect("Customer:customer_vehicle_bookings")

    booking.status = "Rejected"
    booking.save()
    messages.error(request, "Booking rejected.")
    return redirect("Customer:customer_vehicle_bookings")




def mark_contacted(request, booking_id):
    """Mark a booking as 'Contacted' after approval."""
    booking = get_object_or_404(TestDriveBooking, id=booking_id)

    # Ensure only the vehicle owner can update the status
    if request.session.get("cid") != booking.vehicle.owner.id:
        return redirect("Customer:customer_vehicle_bookings")

    booking.Contancted = "Contacted"
    booking.save()
    messages.success(request, "Customer has been marked as Contacted.")
    return redirect("Customer:customer_vehicle_bookings")



def mark_interested(request, booking_id):
    """Update booking interest status to 'Interested'."""
    booking = get_object_or_404(TestDriveBooking, id=booking_id)

    if request.session.get("cid") != booking.customer.id:
        messages.error(request, "Unauthorized action.")
        return redirect("Customer:customer_bookings")

    booking.Intrested = "Intrested"
    booking.save()
    messages.success(request, "Marked as Interested!")
    return redirect("Customer:customer_bookings")


def mark_not_interested(request, booking_id):
    """Update booking interest status to 'Not-Interested'."""
    booking = get_object_or_404(TestDriveBooking, id=booking_id)

    if request.session.get("cid") != booking.customer.id:
        messages.error(request, "Unauthorized action.")
        return redirect("Customer:customer_bookings")

    booking.Intrested = "Not-Intrested"
    booking.save()
    messages.error(request, "Marked as Not Interested.")
    return redirect("Customer:customer_bookings")



def make_payment(request, booking_id):
    """Handle advance payment for test drive booking."""
    booking = get_object_or_404(TestDriveBooking, id=booking_id)

    # Convert price from lakhs to full rupees
    vehicle_price = booking.vehicle.price * Decimal(100000)  # Convert 11.25 → 1125000

    # Calculate 10% advance
    advance_amount = vehicle_price * Decimal(0.1)  # 10% of price

    if request.method == "POST":
        # Assume payment is processed successfully
        booking.payment_status = "Paid"
        booking.Payment_amount = advance_amount  # Store actual advance paid
        booking.save()
        messages.success(request, f"Payment of ₹{advance_amount} successful!")
        return redirect("Customer:customer_bookings")

    return render(
        request,
        "Customer/make_payment.html",
        {
            "booking": booking,
            "vehicle_price_lakh": booking.vehicle.price,  # Still display in Lakhs
            "advance_amount": advance_amount,  # Now correct in Rupees
        },
    )
    
#///////////////////////////////////////////////////////////////////////////////////////////////////////////

def make_rental_payment(request, booking_id):
    """Handle full rental payment processing."""
    booking = get_object_or_404(RentalBooking, id=booking_id)

    # Full rental amount is the vehicle price
    rental_amount = round(booking.vehicle.price, 2)  # No 10% deduction

    if request.method == "POST":
        # Process payment (assume successful)
        booking.payment_status = "Paid"
        booking.Payment_amount = rental_amount  # Store full rental amount
        booking.save()
        messages.success(request, "Rental payment successful!")
        return redirect("Customer:customer_bookings")

    return render(
        request,
        "Customer/rental_payment.html",
        {"booking": booking, "rental_amount": rental_amount},
    )
    
#///////////////////////////////////////////////////////////////////////////////////////////////////////////

def edit_vehicle(request, vehicle_id):
    customer_id = request.session.get('cid')  # Ensure user is logged in
    if not customer_id:
        return redirect("Customer:customer_login")

    vehicle = get_object_or_404(Vehicle, id=vehicle_id, owner_id=customer_id)  # Fetch customer's vehicle

    if request.method == "POST":
        vehicle.title = request.POST["title"]
        vehicle.brand = request.POST["brand"]
        vehicle.model = request.POST["model"]
        vehicle.year = request.POST["year"]
        vehicle.price = request.POST["price"]
        vehicle.fuel_type = request.POST["fuel_type"]
        vehicle.transmission = request.POST["transmission"]
        vehicle.vehicle_type = request.POST["vehicle_type"]
        vehicle.description = request.POST["description"]

        if "image" in request.FILES:
            vehicle.image = request.FILES["image"]

        vehicle.save()
        messages.success(request, "Vehicle updated successfully!")
        return redirect("Customer:customer_vehicles")

    return render(request, "Customer/edit_vehicle.html", {"vehicle": vehicle})


#///////////////////////////////////////////////////////////////////////////////////////////////////////////

def customer_profile(request):
    if "cid" not in request.session:
        return redirect("Customer:customer_login")  # Redirect to login if not authenticated

    customer = get_object_or_404(Customer, id=request.session["cid"])
    return render(request, "Customer/customer_profile.html", {"customer": customer})

# Edit Customer Profile
def edit_customer_profile(request):
    if "cid" not in request.session:
        return redirect("Customer:customer_login")

    customer = get_object_or_404(Customer, id=request.session["cid"])
    
    if request.method == "POST":
        customer.name = request.POST["name"]
        customer.email = request.POST["email"]
        customer.phone = request.POST["phone"]
        customer.address = request.POST["address"]
        
        if "profile_image" in request.FILES:
            customer.profile_image = request.FILES["profile_image"]

        customer.save()
        return redirect("Customer:customer_profile")

    return render(request, "Customer/edit_customer_profile.html", {"customer": customer})

# Change Password
def change_customer_password(request):
    if "cid" not in request.session:
        return redirect("Customer:customer_login")

    customer = get_object_or_404(Customer, id=request.session["cid"])

    if request.method == "POST":
        old_password = request.POST["old_password"]
        new_password = request.POST["new_password"]

        if old_password == customer.password:  # Plain text password check (not secure)
            customer.password = new_password  # Directly updating password (not secure)
            customer.save()
            return redirect("Customer:customer_profile")
        else:
            error = "Incorrect old password."
            return render(request, "Customer/change_customer_password.html", {"error": error})

    return render(request, "Customer/change_customer_password.html")

#///////////////////////////////////////////////////////////////////////////////////////////////////////////

def add_rental_feedback(request, booking_id):
    if "cid" not in request.session:
        return redirect("Customer:Login")

    booking = get_object_or_404(RentalBooking, id=booking_id)

    if request.method == "POST":
        feedback = request.POST["feedback"]
        booking.feedback = feedback  # Store feedback in the model
        booking.save()
        messages.success(request, "Feedback submitted successfully!")
        return redirect("Customer:customer_bookings")

    return render(request, "Customer/add_feedback.html", {"booking": booking})