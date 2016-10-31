from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from ..registration.models import Users
from . import models
from datetime import datetime
from django.db.models import Q
# Create your views here.
def index(request):
    if 'uid' not in request.session:
        messages.error(request, "Please Log in to view your trips.")
        return redirect(reverse('login-main'))
    mytrips = models.UserTrips.objects.filter(user=Users.objects.get(id=request.session['uid']))
    tripid_list = []
    for row in mytrips.values():
        tripid_list.append(row['trip_id'])
    print tripid_list
    othertrips = models.UserTrips.objects.filter(~Q(user=Users.objects.get(id=request.session['uid']))).filter(~Q(trip__id__in = tripid_list))
    context = {'mytrips': mytrips,
               'othertrips': othertrips}
    return render(request,
    'travel/index.html', context)

def destination(request,destid):
    tripinfo = models.Trips.objects.filter(id=destid)
    usersjoined = models.UserTrips.objects.filter(trip__id = destid).filter(~Q(user__id = tripinfo.values()[0]['user_id']))
    context = {'tripinfo': tripinfo,
               'usersjoined': usersjoined}
    return render(request,
    'travel/destination.html', context)

def addtrip(request):
    if 'uid' not in request.session:
        messages.error(request, "Please Log in to add trips.")
        return redirect(reverse('login-main'))

    if request.method == "GET":
        return render(request,
        'travel/addtrip.html')
    elif request.method == "POST":
        destination = request.POST['destination']
        description = request.POST['description']
        dateto = request.POST['dateto']
        datefrom = request.POST['datefrom']
        errors = models.Trips.objects.verify_trip(description = description, destination = destination, dateto = dateto, datefrom = datefrom)
        if errors[0]:
            for error in errors[1]:
                messages.error(request, error)
            return redirect(reverse('travel-add'))
        else:
            dateto = datetime.strptime("{} 00:00:00".format(dateto), "%m/%d/%Y %H:%M:%S")
            datefrom = datetime.strptime("{} 00:00:00".format(datefrom), "%m/%d/%Y %H:%M:%S")
            t = models.Trips(description = description,
                             destination = destination,
                             todate = datefrom,
                             fromdate = dateto,
                             user = Users.objects.get(id=request.session['uid']))
            t.save()
            t2 = models.UserTrips(user=Users.objects.get(id=request.session['uid']),
                                  trip=t)
            t2.save()
            return redirect(reverse('travel-index'))


def usertrip(request,destid):
    if request.method == "GET":
        t = models.UserTrips(user=Users.objects.get(id=request.session['uid']),
                             trip=models.Trips.objects.get(id=destid))
        t.save()
    return redirect(reverse('travel-index'))
