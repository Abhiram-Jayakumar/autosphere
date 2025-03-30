from django.shortcuts import get_object_or_404, render,redirect
from Customer.models import Complaint, Customer, RentalBooking, TestDriveBooking, Vehicle
from Dealer.models import Dealer
from Showroom.models import Showroom
from django.db.models import Count, Sum,Q


def Admin_home(request):
    return render(request,'Admin/Admin_home.html')

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////

def admin_customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'Admin/admin_customer_list.html', {'customers': customers})

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////


def approve_customer(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    customer.approval_status = True
    customer.save()
    return redirect('Admin:admin_customer_list')

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////


def reject_customer(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    customer.approval_status = False
    customer.save()
    return redirect('Admin:admin_customer_list')

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////




def admin_dealer_list(request):
    dealers = Dealer.objects.all()
    return render(request, 'Admin/admin_dealer_list.html', {'dealers': dealers})

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////


def approve_dealer(request, dealer_id):
    dealer = Dealer.objects.get(id=dealer_id)
    dealer.approval_status = True
    dealer.save()
    return redirect('Admin:admin_dealer_list')

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////


def reject_dealer(request, dealer_id):
    dealer = Dealer.objects.get(id=dealer_id)
    dealer.approval_status = False
    dealer.save()
    return redirect('Admin:admin_dealer_list')


#//////////////////////////////////////////////////////////////////////////////////////////////////////////////

def admin_showroom_list(request):
    showrooms = Showroom.objects.all()
    return render(request, 'Admin/admin_showroom_list.html', {'showrooms': showrooms})

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////


def approve_showroom(request, showroom_id):
    showroom = Showroom.objects.get(id=showroom_id)
    showroom.approval_status = True
    showroom.save()
    return redirect('Admin:admin_showroom_list')

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////


def reject_showroom(request, showroom_id):
    showroom = Showroom.objects.get(id=showroom_id)
    showroom.approval_status = False
    showroom.save()
    return redirect('Admin:admin_showroom_list')

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////


def view_complaints(request):
    complaints = Complaint.objects.all().order_by("-submitted_at")
    return render(request, "Admin/view_complaints.html", {"complaints": complaints})

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////


def resolve_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    complaint.status = "Resolved"
    complaint.save()
    return redirect("Admin:view_complaints")

#/////////////////////////////////////////////////////////////////////////////////////////

def admin_dashboard(request):
    total_sale_vehicles = Vehicle.objects.filter(vehicle_type="sale").count()
    total_rental_vehicles = Vehicle.objects.filter(vehicle_type="rent").count()
    total_sales = TestDriveBooking.objects.filter(status="Accepted").count()
    total_rentals = RentalBooking.objects.filter(status="Accepted").count()

    total_sales_revenue = (
        TestDriveBooking.objects.filter(status="Accepted")
        .aggregate(total=Sum("vehicle__price"))["total"] or 0
    )

    total_rental_revenue = (
        RentalBooking.objects.filter(payment_status="Paid")
        .aggregate(total=Sum("vehicle__price"))["total"] or 0
    )

    total_revenue = total_sales_revenue + total_rental_revenue

    top_selling_vehicle = (
        TestDriveBooking.objects.filter(status="Accepted")
        .values("vehicle__model")
        .annotate(count=Count("vehicle"))
        .order_by("-count")
        .first()
    )

    top_selling_dealer = (
        Dealer.objects.annotate(
            total_sales=Count("vehicle__testdrivebooking", filter=Q(vehicle__testdrivebooking__status="Accepted"))
        )
        .values("id", "name", "total_sales")
        .order_by("-total_sales")
        .first()
    )

    top_booking_customer = (
        Customer.objects.annotate(
            total_bookings=Count("testdrivebooking", distinct=True) + Count("rentalbooking", distinct=True)
        )
        .values("id", "name", "total_bookings")
        .order_by("-total_bookings")
        .first()
    )

    context = {
        "total_sale_vehicles": total_sale_vehicles,
        "total_rental_vehicles": total_rental_vehicles,
        "total_sales": total_sales,
        "total_rentals": total_rentals,
        "total_sales_revenue": total_sales_revenue,
        "total_rental_revenue": total_rental_revenue,
        "total_revenue": total_revenue,
        "top_selling_vehicle": top_selling_vehicle,
        "top_selling_dealer": top_selling_dealer,
        "top_booking_customer": top_booking_customer,
    }

    return render(request, "Admin/admin_dashboard.html", context)
