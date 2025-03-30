from django.db import models
from django.utils.timezone import now
from Dealer.models import Dealer
from Showroom.models import Showroom


class Customer(models.Model):  
    name = models.CharField(max_length=100)  
    email = models.EmailField(unique=True)  
    phone = models.CharField(max_length=15, unique=True) 
    registered_at = models.DateTimeField(default=now)  
    approval_status = models.BooleanField(default=False)  
    password = models.CharField(max_length=128)  
    id_proof_number = models.CharField(max_length=50, unique=True)  
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)  
    address = models.TextField()  
    

class Vehicle(models.Model):
    SALE = 'sale'
    RENT = 'rent'
    VEHICLE_TYPES = [
        (SALE, 'For Sale'),
        (RENT, 'For Rent'),
    ]

    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE, null=True, blank=True)
    showroom_dealer = models.ForeignKey(Showroom, on_delete=models.CASCADE, null=True, blank=True)
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True) 

    title = models.CharField(max_length=255)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    vehicle_type = models.CharField(max_length=10, choices=VEHICLE_TYPES, default=SALE) 
    description = models.TextField()
    mileage = models.PositiveIntegerField(null=True, blank=True) 
    fuel_type = models.CharField(max_length=50, choices=[("Petrol", "Petrol"), ("Diesel", "Diesel"), ("Electric", "Electric")])
    transmission = models.CharField(max_length=50, choices=[("Manual", "Manual"), ("Automatic", "Automatic")])
    available = models.BooleanField(default=True) 
    image = models.ImageField(upload_to="vehicle_images/", null=True, blank=True)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.brand} {self.model} - {self.vehicle_type}"
    
    
    
    
class VehicleFeatures(models.Model):
    vehicle = models.OneToOneField(Vehicle, on_delete=models.CASCADE, related_name="features")  
    previous_owners = models.PositiveIntegerField(null=True, blank=True, default=1)
    condition = models.CharField(max_length=50, choices=[("New", "New"), ("Used", "Used")])
    color = models.CharField(max_length=50)
    seating_capacity = models.PositiveIntegerField()
    engine_capacity = models.CharField(max_length=50, null=True, blank=True)  
    fuel_tank_capacity = models.PositiveIntegerField(null=True, blank=True)
    features = models.TextField(null=True, blank=True)  
    safety_rating = models.FloatField(null=True, blank=True)
    gps_enabled = models.BooleanField(default=False)
    bluetooth_connectivity = models.BooleanField(default=False)
    negotiable = models.BooleanField(default=True)
    insurance_valid_till = models.DateField(null=True, blank=True)
    warranty_available = models.BooleanField(default=False)

    def __str__(self):
        return f"Features for {self.vehicle.brand} {self.vehicle.model}"



class TestDriveBooking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)  # Allow null for dealers
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE, null=True, blank=True)  # Optional Dealer field
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=[("Pending", "Pending"), ("Accepted", "Accepted"), ("Rejected", "Rejected")], default="Pending")
    payment_status = models.CharField(max_length=20, choices=[("Pending", "Pending"), ("Paid", "Paid")], default="Pending")
    Payment_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    Contancted = models.CharField(max_length=20, choices=[("Pending", "Pending"), ("Contacted", "Contacted")], default="Pending")
    Intrested = models.CharField(max_length=20, choices=[("Pending", "Pending"), ("Intrested", "Intrested"),("Not-Intrested", "Not-Intrested")], default="Pending")

    
class RentalBooking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    rental_date = models.DateField()
    return_date = models.DateField()
    accessories_needed = models.TextField(blank=True, null=True)  
    status = models.CharField(max_length=20, choices=[("Pending", "Pending"), ("Accepted", "Accepted"), ("Rejected", "Rejected")], default="Pending")
    payment_status = models.CharField(max_length=20, choices=[("Pending", "Pending"), ("Paid", "Paid")], default="Pending")
    feedback = models.TextField(blank=True, null=True) 
    
class Complaint(models.Model):
    ROLE_CHOICES = [
        ("Showroom", "Showroom"),
        ("Customer", "Customer"),
        ("Dealer", "Dealer"),
    ]

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Resolved", "Resolved"),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)  # Role of the complainant
    name = models.CharField(max_length=100)  # Name of the complainant
    address = models.TextField()  # Address of the complainant
    email = models.EmailField()  # Email address
    phone_number = models.CharField(max_length=15)  # Contact number
    complaint_text = models.TextField()  # Complaint details
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Pending")  # Complaint status
    submitted_at = models.DateTimeField(auto_now_add=True)  # Auto timestamp