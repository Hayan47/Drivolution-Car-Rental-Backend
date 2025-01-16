from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser
from .models import Car
from .serializers import CarSerializer
from django.conf import settings
import os
import json


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    parser_classes = [MultiPartParser, JSONParser]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # @method_decorator(cache_page(60 * 60 * 2, key_prefix='cars_list'))
    # def list(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        # Parse the JSON data from the 'data' field
        car_data = json.loads(request.data['data'])

        # Get image files and their primary status
        images_data = []
        for key in request.FILES:
            if key.startswith('images['):
                index = int(key.split('[')[1].split(']')[0])
                images_data.append({
                    'image': request.FILES[key],
                    'is_primary': request.data.get(f'images[{index}]is_primary') == 'true'
                })

        # Add images to the data
        car_data['images'] = images_data

        serializer = self.get_serializer(data=car_data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queryset = Car.objects.all()

        # Filter by availability
        available = self.request.query_params.get('available', None)
        if available is not None:
            queryset = queryset.filter(is_available=available.lower() == 'true')

        # Filter by name
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)

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

            request.build_absolute_uri(f"{settings.MEDIA_URL}car_logos/{file}")
            # request.build_absolute_uri(f"http://192.168.163.77:8000/car_logos/{file}")

            for file in os.listdir(logos_path)
            if os.path.isfile(os.path.join(logos_path, file))
        ]
        return Response(logos)
