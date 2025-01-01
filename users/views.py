from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from .models import User
from cars.models import Car
from cars.serializers import CarSerializer
from .serializers import UserSerializer, RegisterResponseSerializer, EmailTokenObtainPairSerializer, \
    FavoriteCarRequestSerializer, FavoriteCarResponseSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView


@extend_schema(
    request=UserSerializer,
    responses={
        201: RegisterResponseSerializer,
        400: "Bad Request",
    },
    summary="Register a new user",
    description="Allows a new user to register with username, password, phone number, and email."
)
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

    print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(id=self.request.user.id)
        return qs

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @extend_schema(
        request=FavoriteCarRequestSerializer,
        responses={200: FavoriteCarResponseSerializer}
    )
    @action(detail=True, methods=['post'])
    def add_favorite_car(self, request, pk=None):
        user = self.get_object()
        car_id = request.data.get('car_id')
        try:
            car = Car.objects.get(id=car_id)
            user.favorite_cars.add(car)
            return Response({"message": "Car added to favorites"}, status=status.HTTP_200_OK)
        except Car.DoesNotExist:
            return Response({"error": "Car not found"}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        request=FavoriteCarRequestSerializer,
        responses={200: FavoriteCarResponseSerializer}
    )
    @action(detail=True, methods=['post'])
    def remove_favorite_car(self, request, pk=None):
        user = self.get_object()
        car_id = request.data.get('car_id')
        try:
            car = Car.objects.get(id=car_id)
            user.favorite_cars.remove(car)
            return Response({"message": "Car removed from favorites"}, status=status.HTTP_200_OK)
        except Car.DoesNotExist:
            return Response({"error": "Car not found"}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(responses={200: CarSerializer(many=True)})
    @action(detail=True, methods=['get'])
    def favorite_cars(self, request, pk=None):
        user = self.get_object()
        cars = user.favorite_cars.all()
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data)


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer
