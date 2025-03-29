from django.urls import path
from Customer import views



app_name='Customer'



urlpatterns=[

    path('index/',views.index,name='index'),
    path('registration/',views.registartion,name='registration'),
    path('customer_reg/',views.customer_registration,name='customer_reg'),
    path('Customer_home/',views.Customer_home,name='Customer_home'),
    path('Login/',views.login,name='Login'),
    path('add_vehicle/', views.add_vehicle, name='add_vehicle'),
    path('my_vehicles/', views.customer_vehicles, name="customer_vehicles"),
    path('add_vehicle_features/<int:vehicle_id>/',views. add_vehicle_features, name="add_vehicle_features"),
    path('view_vehicles/', views.view_vehicles, name='view_vehicles'),
    path("vehicle_detail/<int:vehicle_id>/", views.vehicle_detail, name="vehicle_detail"),
    path("book_test_drive/<int:vehicle_id>/", views.book_test_drive, name="book_test_drive"),
    path("book_rental/<int:vehicle_id>/", views.book_rental, name="book_rental"),
    path("customer/bookings/", views.customer_bookings, name="customer_bookings"),
    path("my_vehicle_bookings/", views.customer_vehicle_bookings, name="customer_vehicle_bookings"),
    path("approve_booking/<int:booking_id>/", views.approve_customer_booking, name="approve_customer_booking"),
    path("reject_booking/<int:booking_id>/", views.reject_customer_booking, name="reject_customer_booking"),
    path("mark_contacted/<int:booking_id>/", views.mark_contacted, name="mark_contacted"),
    path("make_payment/<int:booking_id>/", views.make_payment, name="make_payment"),
    path("mark_interested/<int:booking_id>/", views.mark_interested, name="mark_interested"),
    path("mark_not_interested/<int:booking_id>/", views.mark_not_interested, name="mark_not_interested"),
    path("make_rental_payment/<int:booking_id>/", views.make_rental_payment, name="make_rental_payment"),
    path("my_vehicles/", views.customer_vehicles, name="customer_vehicles"),
    path("edit_vehicle/<int:vehicle_id>/", views.edit_vehicle, name="edit_vehicle"),
    path("profile/", views.customer_profile, name="customer_profile"),
    path("profile/edit/", views.edit_customer_profile, name="edit_customer_profile"),
    path("profile/change-password/", views.change_customer_password, name="change_customer_password"),
    path("add_rental_feedback/<int:booking_id>/", views.add_rental_feedback, name="add_rental_feedback"),






    
    
    
    ]