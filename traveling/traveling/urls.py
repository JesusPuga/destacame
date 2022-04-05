"""traveling URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from  traveling.views import TravelViewSet, TravelPlanViewSet,  JourneyViewSet, PassengerViewSet, BusViewSet, DriverViewSet, UserViewSet
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r"travel", TravelViewSet)
router.register(r"travel_plan", TravelPlanViewSet)
router.register(r"journey", JourneyViewSet)
router.register(r"passenger", PassengerViewSet)
router.register(r"bus", BusViewSet)
router.register(r"driver", DriverViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
]