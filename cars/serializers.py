from rest_framework import serializers
from .models import Car, CarImage, Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name', 'latitude', 'longitude']


class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ['id', 'image', 'is_primary']


class CarSerializer(serializers.ModelSerializer):
    images = CarImageSerializer(many=True)
    location = LocationSerializer()
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    features = serializers.ListField(
        child=serializers.CharField(max_length=255),
        required=False
    )

    class Meta:
        model = Car
        fields = ['id', 'owner', 'name', 'model', 'interior_color', 'color', 'engine',
                  'kilometrage', 'doors', 'fuel', 'drivetrain', 'logo', 'location',
                  'type', 'transmission', 'seats', 'daily_rate', 'description', 'features', 'images',
                  'created_at', 'updated_at']

    def to_representation(self, instance):
        """Include full car details when serializing"""
        from users.serializers import UserSerializer  # Import here to avoid circular import
        ret = super().to_representation(instance)
        ret['owner'] = UserSerializer(instance.owner).data
        return ret
