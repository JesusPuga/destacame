from django.db import models
from django.utils import timezone
from django.db.models.query import QuerySet

class BaseModelManager(models.Manager):
    def get_queryset(self):
        return QuerySet(self.model, using=self._db).filter(
            disabled_at__isnull=True
        )
# Disabled option is used in all, filter, but avoid in count
class SoftDeletionModel(models.Model):
    disabled_at = models.DateTimeField(blank=True, null=True, editable=False, verbose_name="Desactivar")
    objects = BaseModelManager()

    def delete(self):
        self.disabled_at = timezone.now()
        self.save()

    def hard_delete(self):
        super().delete()

    class Meta:
        abstract = True

class AutoDateMixin(models.Model):
    """ Mixin that auto populates the created and the updated time """

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class CatalogueModel(SoftDeletionModel):
    name = models.CharField(max_length=50, unique=True)
    disabled_at = models.DateTimeField(
        blank=True, null=True, editable=True, verbose_name="Desactivar"
    )

    class Meta:
        abstract = True

    def __str__(self):
        return "{}".format(self.name)

class Driver(CatalogueModel, AutoDateMixin):
    last_name = models.CharField(max_length=50)

class Passenger(CatalogueModel, AutoDateMixin):
    last_name = models.CharField(max_length=50)

class Bus(CatalogueModel, AutoDateMixin):
    seats_amount = models.IntegerField(default=10)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True)

class TravelPlan(CatalogueModel, AutoDateMixin):
    @property
    def avg_passenger(self):
        sum_travels = Travel.objects.filter(travel_plan_id = self.id).count()
        sum_passengers = Journey.objects.filter(travel__travel_plan_id = self.id).count()
        return (sum_passengers / sum_travels) if sum_travels > 0 else 0

    def __str__(self):
        return "{}".format(self.name)

class Travel(SoftDeletionModel, AutoDateMixin):
    travel_plan =  models.ForeignKey(TravelPlan,on_delete=models.SET_NULL, null=True)
    bus = models.ForeignKey(Bus,on_delete=models.SET_NULL, null=True)
    start_date_time = models.DateTimeField()
    finish_date_time = models.DateTimeField()

    @property
    def avg_seats_sold(self):
        amountSold = len(Journey.objects.filter(travel__id = self.id))
        seats_limit = self.bus.seats_amount if self.bus else 10
        return amountSold/seats_limit*100
    

    def __str__(self):
        return "{}".format(self.travel_plan.name)

class Journey(SoftDeletionModel, AutoDateMixin):
    seat_number = models.IntegerField()
    passenger = models.ForeignKey(Passenger,on_delete=models.SET_NULL, null=True)
    travel = models.ForeignKey(Travel,on_delete=models.SET_NULL, null=True)
    