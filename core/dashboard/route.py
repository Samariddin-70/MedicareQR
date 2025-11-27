from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from core.dashboard.forms import RouteForm
from core.models.models import  Route
from src import settings


def route_list(request):
    trips = Route.objects.all()
    paginator = Paginator(trips,settings.LIST_PER_PAGE)
    page = request.GET.get('page',1)
    result = paginator.get_page(page)

    ctx = {
        "result":result,
        "paginator":paginator,
        "status": "list"
    }
    return render(request, 'dashboard/pages/route.html', ctx)


def info(request, pk):
    obj = Route.objects.filter(pk=pk).first()
    if not obj:
        return render(request, 'dashboard/pages/route.html', {"error": 404})
    ctx = {
        "status": "detail",
        "obj": obj,
    }
    return render(request, 'dashboard/pages/route.html', ctx)


def form(request, pk=None):  # edet, add

    obj = None
    if pk:
        obj = Route.objects.filter(pk=pk).first()
        if not obj:
            return render(request,'dashboard/pages/route.html',{"error": 404})
    if request.POST:
        form = RouteForm(request.POST, request.FILES or None, instance=obj)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
        return redirect("route-list")

    ctx = {
        "status": "form",
        "obj": obj,
    }
    return render(request, 'dashboard/pages/route.html', ctx)

def route_delete(request, pk):
    obj = get_object_or_404(Route, id=pk)
    obj.delete()
    return redirect('route-list')
