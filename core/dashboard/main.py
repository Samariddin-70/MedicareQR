from django.shortcuts import render

def index(request):

    ctx={

    }
    return render(request, 'dashboard/pages/index.html', ctx)