from math import floor
from django import forms

from leaflet.forms.widgets import LeafletWidget

class NewEntryForm(forms.Form):

    address = forms.CharField(max_length=50)
    floor = forms.IntegerField(max_value=20)
    rooms = forms.IntegerField(max_value=20)
    area_m_sqrd = forms.FloatField(max_value=300)


    # m = LeafletWidget()
    
