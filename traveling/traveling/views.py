from rest_framework import status, viewsets
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from . import models
from . import serializers
from .filters import TravelAvgFilter

class TravelViewSet(viewsets.ModelViewSet):
    queryset = models.Travel.objects.all()  
    serializer_class = serializers.TravelSerializer
    filterset_class = TravelAvgFilter

class TravelPlanViewSet(viewsets.ModelViewSet):
    queryset = models.TravelPlan.objects.all()
    serializer_class = serializers.TravelPlanSerializer

class JourneyViewSet(viewsets.ModelViewSet):
    queryset = models.Journey.objects.all()
    serializer_class = serializers.JourneySerializer
    filter_fields = ('travel',)

class PassengerViewSet(viewsets.ModelViewSet):
    queryset = models.Passenger.objects.all()
    serializer_class = serializers.PassengerSerializer

class BusViewSet(viewsets.ModelViewSet):
    queryset = models.Bus.objects.all()
    serializer_class = serializers.BusSerializer

class DriverViewSet(viewsets.ModelViewSet):
    queryset = models.Driver.objects.all()
    serializer_class = serializers.DriverSerializer


class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.UserModelSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def login(self, request):
        """User sign in."""
        serializer = serializers.UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': serializers.UserModelSerializer(user).data,
            'access_token': token
        }
        return Response(data, status=status.HTTP_201_CREATED)