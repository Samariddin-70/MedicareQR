from django.urls import path

from core.dashboard import vehicle, trip, route
from core.dashboard.main import index
from core.dashboard.route import route_list
from core.dashboard.user.auth import login, register, logout
from core.dashboard.trip import trip_list

urlpatterns = [
    path('', index, name='dashboard-home'),

    path("register", register, name='dashboard-register'),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),

    #trip crud

    path("trip/", trip_list, name="trip-list"),
    path("trip/detail/<int:pk>/", trip.info, name="trip-info"),
    path("trip/form/add/", trip.form, name="trip-add"),
    path("trip/form/edit/<int:pk>/", trip.form, name="trip-edit"),
    path('trip/delete/<int:pk>/', trip.trip_delete, name='trip-delete'),

    #vehicle crud
    path("vehicle/", vehicle.list, name="vehicle-list"),
    path("vehicle/detail/<int:pk>/", vehicle.info, name="vehicle-info"),
    path("vehicle/form/add/", vehicle.form, name="vehicle-add"),
    path("vehicle/form/edit/<int:pk>/", vehicle.form, name="vehicle-edit"),
    path('vehicle/delete/<int:pk>/', vehicle.vehicle_delete, name='vehicle-delete'),

    #route crud
    path("route/", route_list, name="route-list"),
    path("route/detail/<int:pk>/", route.info, name="route-info"),
    path("route/form/add/", route.form, name="route-add"),
    path("route/form/edit/<int:pk>/", route.form, name="route-edit"),
    path('route/delete/<int:pk>/', route.route_delete, name='route-delete'),

]