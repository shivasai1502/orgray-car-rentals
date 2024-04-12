from django.urls import path
from .views import checkIn_view, checkout, current_bookings, delete_car, login_view, logout_view, home, upload_car_details

urlpatterns = [
    path('checkIn/', checkIn_view, name='checkIn'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('home/', home, name='home'),
    path('checkout/', checkout, name='checkout'),
    path('current_bookings/', current_bookings, name='current_bookings'),
    path('upload-car-details/', upload_car_details, name='upload_car_details'),
    path('delete-car/', delete_car, name='delete_car'),
]

