from . import models
from django.db.models import Q

def includes_dates_range_others_schedules(start, finish, id):
    # includes other ranges between new one
    travels_with_date_time = models.Travel.objects.filter(start_date_time__gte=start, finish_date_time__lte=finish)

    if id:
        travels_with_date_time = travels_with_date_time.filter(~Q(id = id))
    return  len(travels_with_date_time) > 0

def is_date_time_bussy(value, id):
    # is between others date ranges
    travels_with_date_time = models.Travel.objects.filter(start_date_time__lte=value, finish_date_time__gte=value)
    
    if id:
        travels_with_date_time = travels_with_date_time.filter(~Q(id = id))
    return  len(travels_with_date_time) > 0

