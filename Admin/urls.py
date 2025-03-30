
from django.urls import path

from Admin import views

app_name='Admin'

urlpatterns=[
    path('Admin_home/',views.Admin_home,name='Admin_home'),
    path('customers/', views.admin_customer_list, name='admin_customer_list'),
    path('admin/customers/approve/<int:customer_id>/', views.approve_customer, name='approve_customer'),
    path('admin/customers/reject/<int:customer_id>/', views.reject_customer, name='reject_customer'),
    path('admin/dealers/', views.admin_dealer_list, name='admin_dealer_list'),
    path('admin/dealers/approve/<int:dealer_id>/', views.approve_dealer, name='approve_dealer'),
    path('admin/dealers/reject/<int:dealer_id>/', views.reject_dealer, name='reject_dealer'),
    path('admin/showrooms/', views.admin_showroom_list, name='admin_showroom_list'),
    path('admin/showrooms/approve/<int:showroom_id>/', views.approve_showroom, name='approve_showroom'),
    path('admin/showrooms/reject/<int:showroom_id>/', views.reject_showroom, name='reject_showroom'),
    path("view/", views.view_complaints, name="view_complaints"),
    path("resolve/<int:complaint_id>/", views.resolve_complaint, name="resolve_complaint"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),

]