from rest_framework import serializers
from rest_framework.utils import json
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
    features = serializers.ListField(
        child=serializers.CharField(max_length=255),
        required=False
    )
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = ['id', 'owner', 'name', 'model', 'interior_color', 'color', 'engine',
                  'kilometrage', 'doors', 'fuel', 'drivetrain', 'logo', 'location',
                  'type', 'transmission', 'seats', 'daily_rate', 'description', 'features', 'images',
                  'created_at', 'updated_at']

    def create(self, validated_data):
        # Handle nested location
        location_data = validated_data.pop('location')
        location = Location.objects.create(**location_data)

        # Handle images
        images_data = validated_data.pop('images')

        # Create car
        car = Car.objects.create(location=location, **validated_data)

        # Create images
        for image_data in images_data:
            CarImage.objects.create(car=car, **image_data)

        return car

    def validate(self, data):
        # If location is coming as string, parse it
        if isinstance(data.get('location'), str):
            try:
                data['location'] = json.loads(data['location'])
            except json.JSONDecodeError:
                raise serializers.ValidationError({'location': 'Invalid JSON format'})
        return data

    def get_owner(self, obj):
        from users.serializers import UserSerializer  # Import here to avoid circular import
        request = self.context.get('request')
        return UserSerializer(obj.owner, context={'request': request}).data
