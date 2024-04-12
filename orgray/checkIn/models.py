from django.db import models

class Car(models.Model):
    car_model = models.CharField(max_length=255)
    is_available = models.BooleanField(default=True) 

    def __str__(self):
        return self.car_model

class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    mobile_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    drivers_license = models.CharField(max_length=20)
    select_car = models.ForeignKey(Car, on_delete=models.CASCADE)
    checkin_date = models.DateField(auto_now_add=True)
    checkout_date = models.DateField(null=True, blank=True)
