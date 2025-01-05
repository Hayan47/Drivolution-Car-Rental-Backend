from rest_framework import viewsets, status, permissions, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Reservation, Review
from .serializers import ReservationSerializer, ReviewSerializer
from django.db.models import Q


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Reservation.objects.all()
        # Filter by car_id
        car_id = self.request.query_params.get('car_id', None)
        if car_id is not None:
            queryset = queryset.filter(car=car_id)

        # Filter by renter_id
        renter_id = self.request.query_params.get('renter_id', None)
        if renter_id is not None:
            queryset = queryset.filter(renter=renter_id)

        return queryset

    def perform_create(self, serializer):
        car = serializer.validated_data['car']
        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']

        # Check if car is available for the requested dates
        conflicting_reservations = Reservation.objects.filter(
            car=car,
            status__in=['PENDING', 'CONFIRMED', 'ACTIVE'],
            start_date__lt=end_date,
            end_date__gt=start_date
        )

        if conflicting_reservations.exists():
            raise serializers.ValidationError(
                "Car is not available for the selected dates."
            )

        # Calculate total cost
        days = (end_date - start_date).days
        total_cost = days * car.daily_rate

        serializer.save(
            renter=self.request.user,
            total_cost=total_cost,
            status='PENDING'
        )

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        reservation = self.get_object()
        if reservation.car.owner != request.user:
            return Response(
                {"error": "Only car owner can confirm reservation"},
                status=status.HTTP_403_FORBIDDEN
            )
        reservation.status = 'CONFIRMED'
        reservation.save()
        return Response(self.get_serializer(reservation).data)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        reservation = self.get_object()
        if reservation.renter != request.user:
            return Response(
                {"error": "Only renter can cancel reservation"},
                status=status.HTTP_403_FORBIDDEN
            )
        reservation.status = 'CANCELLED'
        reservation.save()
        return Response(self.get_serializer(reservation).data)
