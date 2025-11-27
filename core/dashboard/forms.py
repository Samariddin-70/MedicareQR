from django import forms

from core.models.models import Vehicle, Route, Trip


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = "__all__"

class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = "__all__"

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = "__all__"