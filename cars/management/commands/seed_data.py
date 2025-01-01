from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from cars.models import Car, CarImage
from reservations.models import Reservation
from django.utils import timezone
from datetime import timedelta
import random

User = get_user_model()

