from django.db import models
from users.models import User


class Location(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.name


class Car(models.Model):
    TRANSMISSION_CHOICES = [
        ('AUTOMATIC', 'Automatic'),
        ('MANUAL', 'Manual'),
    ]
    TYPE_CHOICES = [
        ('SEDAN', 'Sedan'),
        ('PICKUP', 'PickUp'),
        ('SUV', 'SUV'),
        ('SPORT', 'Sport'),
        ('COUPE', 'Coupe'),
        ('CONVERTIBLE', 'Convertible'),
        ('HATCHBACK', 'HatchBack'),
    ]
    FUELS_CHOICES = [
        ('PETROL', 'Petrol'),
        ('DIESEL', 'Diesel'),
        ('ELECTRIC', 'Electric'),
        ('HYBRID', 'Hybrid'),
    ]
    DRIVETRAIN_CHOICES = [
        ('FWD', 'FWD'),
        ('RWD', 'RWD'),
        ('AWD', 'AWD'),
        ('4WD', '4WD'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_cars')
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    interior_color = models.CharField(max_length=50)
    engine = models.CharField(max_length=50)
    kilometrage = models.IntegerField()
    logo = models.URLField()
    transmission = models.CharField(max_length=12, choices=TRANSMISSION_CHOICES)
    type = models.CharField(max_length=12, choices=TYPE_CHOICES)
    fuel = models.CharField(max_length=12, choices=FUELS_CHOICES)
    drivetrain = models.CharField(max_length=12, choices=DRIVETRAIN_CHOICES)
    seats = models.IntegerField()
    doors = models.IntegerField()
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='cars')
    description = models.TextField()
    features = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} {self.model}"


class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='car_images/')
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.car.name} {self.car.model}"
