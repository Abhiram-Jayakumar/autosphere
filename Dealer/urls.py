



from django.urls import path
from Dealer import views


app_name='Dealer'

urlpatterns=[
      path('Dealer_reg/',views.dealer_registration,name='Dealer_reg'),
      path('Dealer_home/',views.Dealer_home,name='Dealer_home'),
      path('add_vehicle/', views.add_vehicle, name='add_vehicle'),
      path('my_vehicles/', views.dealer_vehicles, name="dealer_vehicles"),
      path('add_vehicle_features/<int:vehicle_id>/', views.add_vehicle_features, name="add_vehicle_features"),
      path("bookings/", views.dealer_bookings, name="dealer_bookings"),
      path("approve_booking/<str:booking_type>/<int:booking_id>/", views.approve_dealer_booking, name="approve_dealer_booking"),
      path("reject_booking/<str:booking_type>/<int:booking_id>/", views.reject_dealer_booking, name="reject_dealer_booking"),
      path("vehicles/", views.dealer_vehicle_list, name="dealer_vehicle_list"),
      path("vehicle/<int:vehicle_id>/", views.dealer_vehicle_detail, name="dealer_vehicle_detail"),
      path("book_test_drive/<int:vehicle_id>/", views.book_test_drive_for_dealer, name="book_test_drive"),
      path("Dealer_booked_vehicel/", views.Dealer_booked_vehicel, name="Dealer_booked_vehicel"),
      path("mark_interested/<int:booking_id>/", views.mark_interested_dealer, name="mark_interested_dealer"),
      path("mark_not_interested/<int:booking_id>/", views.mark_not_interested_dealer, name="mark_not_interested_dealer"),
      path("make_payment/<int:booking_id>/", views.make_payment_dealer, name="make_payment_dealer"),
      path("mark_as_contacted/<int:booking_id>/", views.mark_as_contacted, name="mark_as_contacted"),
      path("edit_dealer_vehicle/<int:vehicle_id>/", views.edit_dealer_vehicle, name="edit_dealer_vehicle"),
      path("dealer_profile/", views.dealer_profile, name="dealer_profile"),
      path("edit_dealer_details/", views.edit_dealer_details, name="edit_dealer_details"),
      path("change_dealer_password/", views.change_dealer_password, name="change_dealer_password"),
      path("dashboard/", views.dealer_dashboard, name="dealer_dashboard"),



      





]