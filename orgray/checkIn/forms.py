from django.utils import timezone
import re
from django import forms
from .models import Car, Customer

class AlphabetValidator:
    def __init__(self, message="Only alphabets are allowed."):
        self.message = message

    def __call__(self, value):
        if not re.match("^[a-zA-Z\s]*$", value):
            raise forms.ValidationError(self.message)
        
class NumericValidator:
    def __init__(self, message="Only numeric characters are allowed."):
        self.message = message

    def __call__(self, value):
        if not re.match("^[0-9]*$", value):
            raise forms.ValidationError(self.message)
        
class CheckInForm(forms.ModelForm):
    checkout_date = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'Enter Expected Checkout Date', 'class': 'datepicker', 'autocomplete': 'off'}))
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'Enter Date of Birth', 'class': 'datepicker', 'autocomplete': 'off'}))
    mobile_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Mobile Number', 'autocomplete': 'off'}), validators=[NumericValidator()])
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter First Name', 'autocomplete': 'off'}), validators=[AlphabetValidator()])
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Last Name', 'autocomplete': 'off'}), validators=[AlphabetValidator()])
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Address', 'autocomplete': 'off'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter City', 'autocomplete': 'off'}))
    state = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter State', 'autocomplete': 'off'}))
    drivers_license = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Driver\'s License Number', 'autocomplete': 'off'}))
    select_car = forms.ModelChoiceField(queryset=Car.objects.filter(is_available=True))

    class Meta:
        model = Customer
        exclude = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically set the choices for the select_car field based on available cars
        available_cars = Car.objects.filter(is_available=True)
        self.fields['select_car'].widget.choices = [(car.id, car.car_model) for car in available_cars]

    def clean(self):
        cleaned_data = super().clean()
        checkout_date = cleaned_data.get('checkout_date')
        checkin_date = cleaned_data.get('checkin_date')

        # Check if checkout date is greater than or equal to the current date
        current_date = timezone.now().date()
        if checkout_date < current_date:
            raise forms.ValidationError('Checkout date must be greater than or equal to the current date.')

        return cleaned_data


class CheckOutForm(forms.ModelForm):
    checkout_date = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'Enter Checkout Date', 'class': 'datepicker', 'autocomplete': 'off'}))
    cost_per_day = forms.DecimalField(widget=forms.TextInput(attrs={'autocomplete': 'off', 'placeholder': 'Enter Cost Per Day'}))
    mobile_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Mobile Number', 'autocomplete': 'off'}), validators=[NumericValidator()])

    class Meta:
        model = Customer
        fields = ['mobile_number', 'checkout_date', 'cost_per_day']



class CarForm(forms.ModelForm):
    car_model = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Car Name', 'autocomplete': 'off'}))
    class Meta:
        model = Car
        fields = ['car_model', 'is_available']

