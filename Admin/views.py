from django.shortcuts import render,redirect
from Customer.models import Customer
from Dealer.models import Dealer
from Showroom.models import Showroom





def Admin_home(request):
    return render(request,'Admin/Admin_home.html')

##########customer approvel  views################

def admin_customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'Admin/admin_customer_list.html', {'customers': customers})

def approve_customer(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    customer.approval_status = True
    customer.save()
    return redirect('Admin:admin_customer_list')

def reject_customer(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    customer.approval_status = False
    customer.save()
    return redirect('Admin:admin_customer_list')

##############dealer approvel######################




def admin_dealer_list(request):
    dealers = Dealer.objects.all()
    return render(request, 'Admin/admin_dealer_list.html', {'dealers': dealers})

def approve_dealer(request, dealer_id):
    dealer = Dealer.objects.get(id=dealer_id)
    dealer.approval_status = True
    dealer.save()
    return redirect('Admin:admin_dealer_list')

def reject_dealer(request, dealer_id):
    dealer = Dealer.objects.get(id=dealer_id)
    dealer.approval_status = False
    dealer.save()
    return redirect('Admin:admin_dealer_list')


###########showroom approvel###############

def admin_showroom_list(request):
    showrooms = Showroom.objects.all()
    return render(request, 'Admin/admin_showroom_list.html', {'showrooms': showrooms})

def approve_showroom(request, showroom_id):
    showroom = Showroom.objects.get(id=showroom_id)
    showroom.approval_status = True
    showroom.save()
    return redirect('Admin:admin_showroom_list')

def reject_showroom(request, showroom_id):
    showroom = Showroom.objects.get(id=showroom_id)
    showroom.approval_status = False
    showroom.save()
    return redirect('Admin:admin_showroom_list')