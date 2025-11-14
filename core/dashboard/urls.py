from django.urls import path

from core.dashboard.main import index

urlpatterns = [
    path('', index, name='dashboard-home'),
]