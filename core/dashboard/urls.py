from django.urls import path

from core.dashboard.views import index

urlpatterns = [
    path('', index, name='dashboard-home'),
]