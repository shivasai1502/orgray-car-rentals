from django import forms
from django.shortcuts import render, redirect
from .forms import CheckInForm
from django.utils.crypto import get_random_string
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render
from .models import Customer
from .forms import CheckOutForm
from django.shortcuts import render, redirect
from .models import Car
from .forms import CarForm
from django.shortcuts import get_object_or_404



@login_required(login_url='/login/')
def checkIn_view(request):
    if request.method == 'POST':
        form = CheckInForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            
            # Get the selected car model from the form data
            selected_car_model = form.cleaned_data['select_car']

            # Get the corresponding Car instance
            selected_car_instance = get_object_or_404(Car, car_model=selected_car_model)

            # Assign the Car instance to the select_car field
            customer.select_car = selected_car_instance
            customer.save()

            # Update availability status
            selected_car_instance.is_available = False
            selected_car_instance.save()

            return render(request, 'checkIn/success.html', {'form': form})
    else:
        form = CheckInForm()

    return render(request, 'checkIn/checkIn.html', {'form': form})


@login_required(login_url='/login/')
def home(request):
    available_cars = Car.objects.filter(is_available=True)
    return render(request, 'checkIn/home.html', {'available_cars': available_cars})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'checkIn/login.html', {'form': form})


@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logging out


@login_required(login_url='/login/')
def checkout(request):
    if request.method == 'POST':
        form = CheckOutForm(request.POST)
        if form.is_valid():
            mobile_number = form.cleaned_data['mobile_number']
            checkout_date = form.cleaned_data['checkout_date']
            cost_per_day = form.cleaned_data['cost_per_day']
            try:
                checkin_entry = Customer.objects.get(mobile_number=mobile_number)
            except Customer.DoesNotExist:
                return render(request, 'checkIn/checkout.html', {'form': form, 'error': 'User not found.'})
            
            if checkout_date <= checkin_entry.checkin_date:
                raise forms.ValidationError('Checkout date must be greater than the check-in date.')

            # Update the checkout date in the model
            checkin_entry.checkout_date = checkout_date
            checkin_entry.save()

            # Calculate the number of days between check-in and check-out
            num_days = (checkout_date - checkin_entry.checkin_date).days

            # Calculate total cost
            total_cost = num_days * cost_per_day
            selected_car = checkin_entry.select_car
            selected_car.is_available = True
            selected_car.save()

            # Delete the corresponding row from the database
            checkin_entry.delete()
            

            return render(request, 'checkIn/checkout_summary.html', {
                'checkin_entry': checkin_entry,
                'checkout_date': checkout_date,
                'num_days': num_days,
                'total_cost': total_cost,
            })

    else:
        form = CheckOutForm()

    return render(request, 'checkIn/checkout.html', {'form': form})


# views.py
@login_required(login_url='/login/')
def current_bookings(request):
    bookings = Customer.objects.all()
    return render(request, 'checkIn/bookings.html', {'bookings': bookings})

@login_required(login_url='/login/')
def upload_car_details(request):
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('upload_car_details')  # Redirect to the same page after successful upload
    else:
        form = CarForm()

    return render(request, 'checkIn/uploadcars.html', {'form': form})

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Car

@login_required(login_url='/login/')
def delete_car(request):
    cars = Car.objects.all()

    if request.method == 'POST':
        action = request.POST.get('action')
        selected_cars = request.POST.getlist('selected_cars')

        if action == 'delete':
            # Handle the selected cars for deletion
            Car.objects.filter(id__in=selected_cars).delete()

        elif action == 'make_available':
            # Make selected cars available
            Car.objects.filter(id__in=selected_cars).update(is_available=True)

        elif action == 'make_unavailable':
            # Make selected cars unavailable
            Car.objects.filter(id__in=selected_cars).update(is_available=False)

    return render(request, 'checkIn/carslist.html', {'cars': cars})
