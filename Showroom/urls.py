



from django.urls import path
from Showroom import views


app_name='Showroom'

urlpatterns=[
        path('Showroom_reg/',views.showroom_registration,name='Showroom_reg'),
        path('Showroom_home/',views.Showroom_home,name='Showroom_home'),
        path('add_vehicle/', views.add_vehicle, name='add_vehicle'),
        path('showroom_vehicles/', views.showroom_vehicles, name="showroom_vehicles"),
        path('add_vehicle_features/<int:vehicle_id>/', views.add_vehicle_features, name="add_vehicle_features"),
        path("bookings/", views.showroom_bookings, name="showroom_bookings"),
        path("approve_booking/<str:booking_type>/<int:booking_id>/", views.approve_booking, name="approve_booking"),
        path("reject_booking/<str:booking_type>/<int:booking_id>/", views.reject_booking, name="reject_booking"),
        path("mark_contacted/<int:booking_id>/", views.mark_contacted, name="mark_contacted"),
        path("showroom_vehicles/", views.showroom_vehicles, name="showroom_vehicles"),
        path("edit_vehicle/<int:vehicle_id>/", views.edit_vehicle, name="edit_vehicle"),
        path("profile/", views.showroom_profile, name="showroom_profile"),
        path("edit_profile/", views.edit_showroom_profile, name="edit_showroom_profile"),
        path("change_password/", views.change_showroom_password, name="change_showroom_password"),
        path("dashboard/", views.showroom_dashboard, name="showroom_dashboard"),

        
       

]