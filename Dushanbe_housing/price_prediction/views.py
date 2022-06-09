from http.client import NON_AUTHORITATIVE_INFORMATION
from turtle import width
from django.shortcuts import render, HttpResponse
from price_prediction.forms import NewEntryForm
from geopy import Nominatim
import xgboost
import pickle
# from geopy.geocoders import Nomination

# import folium
def get_geo(address):
    add = str(address)+", Dushanbe, Tajikistan"
    locator = Nominatim(user_agent="myGeocoder")
    location = locator.geocode(add)
    return location
# Create your views here.
filename = "xgboost_model.sav"
model = pickle.load(open(filename, 'rb'))

def index(request):
    form = NewEntryForm(request.POST or None)
    # ip = "72.14.207.99"
    # m = folium.Map(width=800, height=500,location=(38.566940, 68.781236))
    # m = m._repr_html_()
    context = {
        'form':form,
        'message':None,
    }
    if request.POST:
        print("was posted!")
        if form.is_valid():

            temp = form.cleaned_data.get("address")
            geo = get_geo(temp)
            if geo == None:
                context['message'] = "Not a valid adress"
            else:
                rooms = form.cleaned_data.get("rooms")
                floor = form.cleaned_data.get("floor")
                area_m_sqrd = form.cleaned_data.get("area_m_sqrd")
                latitude = geo.latitude
                longitude = geo.longitude
                parameters = [[rooms,floor,area_m_sqrd,latitude,longitude]]
                prediction = model.predict(parameters)
                print("Hello Man!")
                print(prediction)
                context['message'] = prediction
            

    return render(request,"index.html",context=context)
