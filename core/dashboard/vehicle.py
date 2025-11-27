from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from core.dashboard.forms import VehicleForm
from core.models.models import Vehicle
from src import settings


def list(request):
    trips = Vehicle.objects.all()
    paginator = Paginator(trips,settings.LIST_PER_PAGE)
    page = request.GET.get('page',1)
    result = paginator.get_page(page)

    ctx = {
        "result":result,
        "paginator":paginator,
        "status":"list"
    }
    return render(request,'dashboard/pages/vehicle.html',ctx)

def info(request, pk):
    obj = Vehicle.objects.filter(pk=pk).first()
    if not obj:
        return render(request,'dashboard/pages/vehicle.html',{"error": 404})
    ctx={
        "status" : "detail",
        "obj":obj,
    }
    return render(request,'dashboard/pages/vehicle.html',ctx)

def form(request, pk=None): #edet, add

    obj = None
    if pk:
        obj = Vehicle.objects.filter(pk=pk).first()
        if not obj:
            return render(request,'dashboard/pages/vehicle.html',{"error": 404})
    if request.POST:
        print(">>>>>", request.POST)
        form = VehicleForm(request.POST, request.FILES or None, instance=obj)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
        return redirect("vehicle-list")

    ctx={
        "status" : "form",
        "vehicle_types": Vehicle.VEHICLE_TYPES,
        "obj":obj,
    }
    return render(request,'dashboard/pages/vehicle.html',ctx)

def vehicle_delete(request, pk):
    obj = get_object_or_404(Vehicle, id=pk)
    obj.delete()
    return redirect('route-list')