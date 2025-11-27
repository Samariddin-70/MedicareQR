from django.shortcuts import render


def register(request):
    ctx={

    }
    return render()

def login(request):
    ctx={

    }
    return render(request,"user/login.html", ctx)

def logout(request):

    return render("login")