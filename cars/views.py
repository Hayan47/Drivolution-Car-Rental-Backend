from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Car, CarImage
from .serializers import CarSerializer, CarImageSerializer
from django.conf import settings
import os
from rest_framework.views import APIView
from rest_framework.response import Response


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queryset = Car.objects.all()

        # Filter by availability
        available = self.request.query_params.get('available', None)
        if available is not None:
            queryset = queryset.filter(is_available=available.lower() == 'true')

        # Filter by location
        location = self.request.query_params.get('location', None)
        if location:
            queryset = queryset.filter(location__name__icontains=location)

        # Filter by price range
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        if min_price:
            queryset = queryset.filter(daily_rate__gte=float(min_price))
        if max_price:
            queryset = queryset.filter(daily_rate__lte=float(max_price))

        return queryset

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_cars(self, request):
        cars = Car.objects.filter(owner=request.user)
        serializer = self.get_serializer(cars, many=True)
        return Response(serializer.data)


class StaticCarLogoListAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        logos_path = os.path.join(settings.MEDIA_ROOT, 'car_logos')
        logos = [

            # request.build_absolute_uri(f"{settings.MEDIA_URL}car_logos/{file}")
            request.build_absolute_uri(f"http://192.168.163.77:8000/car_logos/{file}")

            for file in os.listdir(logos_path)
            if os.path.isfile(os.path.join(logos_path, file))
        ]
        return Response(logos)
