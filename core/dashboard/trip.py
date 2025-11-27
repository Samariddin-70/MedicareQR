from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from core.dashboard.forms import TripForm
from core.models.models import Trip, Vehicle, Route
from src import settings


def trip_list(request):
    trips = Trip.objects.all()
    paginator = Paginator(trips,settings.LIST_PER_PAGE)
    page = request.GET.get('page',1)
    result = paginator.get_page(page)

    ctx = {
        "result":result,
        "paginator":paginator,
        "status": "list"
    }
    return render(request, 'dashboard/pages/trip.html', ctx)


def info(request, pk):
    obj = Trip.objects.filter(pk=pk).first()
    if not obj:
        return render(request, 'dashboard/pages/trip.html', {"error": 404})
    ctx = {
        "status": "detail",
        "obj": obj,
    }
    return render(request, 'dashboard/pages/trip.html', ctx)


def form(request, pk=None):  # edet, add

    obj = None
    if pk:
        obj = Trip.objects.filter(pk=pk).first()
        if not obj:
            return render(request, 'dashboard/pages/trip.html', {"error": 404})
    if request.POST:
        form = TripForm(request.POST, request.FILES or None, instance=obj)
        if form.is_valid():
            form.save()
        else:
            print(">>>>trip", form.errors, f"\n\n>>>>>>>: {request.POST}\n\n")
        return redirect("trip-list")


    ctx = {
        "status": "form",
        "obj": obj,
        "vehicle_types": Vehicle.objects.all().order_by('vehicle_type'),
        "routes": Route.objects.all().order_by('name')
    }
    return render(request, 'dashboard/pages/trip.html', ctx)

def trip_delete(request, pk):
    obj = get_object_or_404(Trip, id=pk)
    obj.delete()
    return redirect('route-list')

