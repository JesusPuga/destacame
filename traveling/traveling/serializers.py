from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.db.models import Q
from . import models
from . import utils

class BusSerializer(serializers.ModelSerializer):
    driver_name = serializers.CharField(source="driver.name", default=None, read_only=True)
    class Meta:
        model = models.Bus
        fields = ("id","name","driver", "driver_name", "seats_amount")
        read_only_fields = ("id",)

    def validate(self, data):
        buses = models.Bus.objects.filter(driver=data.get("driver",0))
        # Avoid record updated in condition
        if self.instance:
            buses = buses.filter(~Q(id = self.instance.id))

        if len(buses) > 0:
            raise serializers.ValidationError("El conductor ya está asignado a otro autobús")
        return data


class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Passenger
        fields = "__all__"
        read_only_fields = ("id",)

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Driver
        fields = "__all__"
        read_only_fields = ("id",)

class TravelSerializer(serializers.ModelSerializer):
    bus_name = serializers.CharField(source="bus.name", default=None, read_only=True)
    travel_plan_name = serializers.CharField(source="travel_plan.name", default=None, read_only=True)
    start_date_time = serializers.DateTimeField()
    finish_date_time = serializers.DateTimeField()
    avg_seats_sold = serializers.ReadOnlyField()

    class Meta:
        model = models.Travel
        fields = ("id", "start_date_time", "finish_date_time", "bus","bus_name", "travel_plan", "travel_plan_name", "avg_seats_sold")
        read_only_fields = ("id", "avg_seats_sold")

    def validate_start_date_time(self, value):
        id = self.instance.id if self.instance else None
        if utils.is_date_time_bussy(value, id):
            raise serializers.ValidationError("La fecha/hora de inicio está ocupada")
        return value

    def validate_finish_date_time(self, value):
        id = self.instance.id if self.instance else None
        if utils.is_date_time_bussy(value, id):
            raise serializers.ValidationError("La fecha/hora de fin está ocupada")
        return value

    def validate(self, data):
        id = self.instance.id if self.instance else None

        if data['start_date_time'] > data['finish_date_time']:
            raise serializers.ValidationError("La fecha/hora fin debe ser mayor a la de inicio")

        if data['start_date_time'] == data['finish_date_time']:
            raise serializers.ValidationError("Las fecha/hora no pueden ser iguales")

        if utils.includes_dates_range_others_schedules(data['start_date_time'] , data['finish_date_time'], id):
            raise serializers.ValidationError("Ambas fecha/hora incluyen otros horarios")

        return data

class TravelPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TravelPlan
        fields = ("id", "name", "avg_passenger")
        read_only_fields = ("id", "avg_passenger")

class JourneySerializer(serializers.ModelSerializer):
    passenger_name = serializers.CharField(source="passenger.name", default=None, read_only=True)
    travel_name = serializers.CharField(source="travel.travel_plan.name", default=None, read_only=True)

    class Meta:
        model = models.Journey
        fields = ("id", "passenger", "passenger_name", "seat_number", "travel", "travel_name", "disabled_at")
        read_only_fields = ("id",)

    def validate(self, data):
        seats_used = models.Journey.objects.filter(travel=data["travel"])
        seats_allowed = data["travel"].bus.seats_amount
        # Check amount limit in create
        if len(seats_used) >= seats_allowed and not self.instance:
            raise serializers.ValidationError("El autobús ya está lleno")

        if data['seat_number'] > seats_allowed or data['seat_number'] == 0:
            raise serializers.ValidationError("El rango permitido es de 1-{0}".format(seats_allowed))
   
        seats = models.Journey.objects.filter(seat_number=data['seat_number'], travel=data["travel"])

        # Avoid record updated in condition
        if self.instance:
            seats = seats.filter(~Q(id = self.instance.id))
      
        if len(seats) > 0:
            raise serializers.ValidationError("El asiento ya está siendo usado")

        return data


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:

        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Las credenciales no son válidas')

        self.context['user'] = user
        return data

    def create(self, data):
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key