from django.shortcuts import render

def index(request):
    ctx={

    }
    return render(request, 'dashboard/base.html', ctx)