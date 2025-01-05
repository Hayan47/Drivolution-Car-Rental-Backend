from django.db import models
from users.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


class Location(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.DecimalField(
        max_digits=20,  # Total number of digits
        decimal_places=15,  # Number of digits after the decimal point
        validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)],
        help_text="Latitude must be between -90 and 90."
    )
    longitude = models.DecimalField(
        max_digits=20,  # Total number of digits
        decimal_places=15,  # Number of digits after the decimal point
        validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)],
        help_text="Longitude must be between -180 and 180."
    )

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
    description = models.TextField(null=True, blank=True)
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
