from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# @login_required(login_url="login")
def index(request):

    ctx={

    }
    return render(request, 'dashboard/pages/index.html', ctx)