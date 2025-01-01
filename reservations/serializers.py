from rest_framework import serializers
from .models import Reservation, Review
from cars.serializers import CarSerializer
from users.serializers import UserSerializer


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'rating', 'comment', 'created_at']


class ReservationSerializer(serializers.ModelSerializer):
    review = ReviewSerializer(read_only=True)
    car_details = CarSerializer(source='car', read_only=True)
    renter_details = UserSerializer(source='renter', read_only=True)

    class Meta:
        model = Reservation
        fields = ['id', 'renter', 'car', 'car_details', 'renter_details',
                  'start_date', 'end_date', 'status', 'total_cost',
                  'review', 'created_at', 'updated_at']
        read_only_fields = ['status', 'total_cost']
        extra_kwargs = {
            'renter': {'required': False}
        }
