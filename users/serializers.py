from rest_framework import serializers
from cars.serializers import CarSerializer
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password as django_validate_password
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    favorite_cars = CarSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'profile_picture',
                  'date_of_birth', 'password', 'is_verified', 'favorite_cars']
        read_only_fields = ['is_verified']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
            'email': {'required': True}
        }

    def validate_password(self, value):
        try:
            django_validate_password(value)
            return value
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class RegisterResponseSerializer(serializers.Serializer):
    user = UserSerializer()
    refresh = serializers.CharField()
    access = serializers.CharField()


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError({
                'error': 'Both email and password are required.'
            })

        user = authenticate(email=email, password=password)

        if not user:
            user_exists = User.objects.filter(email=email).exists()
            if user_exists:
                raise serializers.ValidationError({
                    'password': 'Invalid password. Please try again.'
                })
            else:
                raise serializers.ValidationError({
                    'email': 'No account found with this email.'
                })

        if not user.is_active:
            raise serializers.ValidationError({
                'error': 'This account is inactive.'
            })

        data = super().validate(attrs)
        user_data = UserSerializer(user).data
        data.update({
            'user': user_data,
        })
        return data


class FavoriteCarRequestSerializer(serializers.Serializer):
    car_id = serializers.IntegerField()


class FavoriteCarResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
