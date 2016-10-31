from __future__ import unicode_literals
from ..registration.models import Users
from django.db import models
from datetime import datetime

class TripsManager(models.Manager):
    def verify_trip(self, **kwargs):
        errors = False
        error_list = []
        if [required for required in ['description','destination','dateto','datefrom'] if required in kwargs.keys()]:
            for key in kwargs.keys():
                if kwargs[key] == "":
                    errors = True
                    error_list.append("{} field missing!".format(key))
            today = datetime.today().date()
            try:
                dateto = datetime.strptime("{} 00:00:00".format(kwargs['dateto']), "%m/%d/%Y %H:%M:%S")
                datefrom = datetime.strptime("{} 00:00:00".format(kwargs['datefrom']), "%m/%d/%Y %H:%M:%S")
                if dateto.date() < today:
                    errors = True
                    error_list.append("To date is less than today!")
                if datefrom.date() < today:
                    errors = True
                    error_list.append("From date is less than today!")

                if dateto.date() > datefrom.date():
                    errors = True
                    error_list.append("From Date is greater than To Date!")
            except Exception, e:
                print (e)
                errors = True
                error_list.append("Date Fields are invalid. Please Try again.")
        else:
            errors = True
            error_list.append("Some fields were not passed to registertrips method. Please try again.")
        if errors:
            return (True, error_list)
        else:
            return (False, "Review Added!")

# Create your models here.
class Trips(models.Model):
    description = models.TextField()
    destination = models.CharField(max_length = 255)
    todate = models.DateTimeField()
    fromdate = models.DateTimeField()
    user = models.ForeignKey(Users)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = TripsManager()

    class Meta:
        managed = False
        db_table = 'trips'

class UserTrips(models.Model):
    user = models.ForeignKey(Users, related_name="userontrip")
    trip = models.ForeignKey(Trips, related_name="userstripid")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        managed = False
        db_table = 'user_trips'
