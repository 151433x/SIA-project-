# Your API KEYS (you need to use your own keys - very long random characters)
from pprint import pprint
from config import MAPQUEST_API_KEY, MBTA_API_KEY,ATTOM_API_KEY
import urllib.request
import json
import http.client 

def property_detailer(address_number,address_2):
    """"this will take in two forms, one main address and then one city, and state. from there it will return the entire json of information about the property"""
    conn = http.client.HTTPSConnection("api.gateway.attomdata.com")
    address_number=address_number.replace(' ','%20')
    address_2=address_2.replace(',','%2C')
    address_2=address_2.replace(' ','%20')
    headers = { 
        'accept': "application/json", 
        'apikey': ATTOM_API_KEY 
    } 
    conn.request("GET", f"/propertyapi/v1.0.0/property/detail?address1={address_number}&address2={address_2}", headers=headers)
    res = conn.getresponse() 
    data = res.read()
    result=json.loads(data.decode("utf-8"))
    return result
def postcode(address_number,address_2):
    """this function will take 2 inputs one address_number and adresss 2 which is just the 'city,state', from there it will get the postal code of the property."""
    result =property_detailer(address_number,address_2)['property'][0]['address']['postal1']
    return result
def properties_around(address_number,address_2):
    property_detailer(address_number,address_2)


# Useful URLs (you need to add the appropriate parameters for your requests)
MAPQUEST_BASE_URL = "http://www.mapquestapi.com/geocoding/v1/address"
MBTA_BASE_URL = "https://api-v3.mbta.com/stops"
MBTA_DISTANCE_URL=''
MAPQUEST_GUI_URL='http://open.mapquestapi.com/guidance/v2/route'
# A little bit of scaffolding if you want to use it
# upload api and hide 

def get_json(url):
    """
    Given a properly formatted URL for a JSON web API request, return
    a Python JSON object containing the response to that request.

    Both get_lat_long() and get_nearest_station() might need to use this function.
    """
    f = urllib.request.urlopen(url)
    response_text = f.read().decode('utf-8')
    response_data = json.loads(response_text)
    return response_data   
def get_lat_long(place_name):
    """
    Given a place address, return a (latitude, longitude) tuple
    with the coordinates of the given place.
    See https://developer.mapquest.com/documentation/geocoding-api/address/get/
    for Mapquest Geocoding API URL formatting requirements.
    """
    place_name=place_name.replace(' ','%20')+',MA'
    mapquest_pull=f'{MAPQUEST_BASE_URL}?key={MAPQUEST_API_KEY}&location={place_name}&boundingBox=42.4601311,-71.3159173,42.1755041,-70.8542204' 
    data=dict(get_json(mapquest_pull))
    lat=data['results'][0]['locations'][0]['latLng']['lat']
    lng=data['results'][0]['locations'][0]['latLng']['lng']
    return lat,lng
def open_guy(location1,location2,):
    location1=location1.replace(' ','+')
    location2=location2.replace(' ','+')
    mapquest_gui_pull=f'{MAPQUEST_GUI_URL}?key={MAPQUEST_API_KEY}&from={location1}&to={location2}&routeType=pedestrian&narrativeType=text' 
    data=dict(get_json(mapquest_gui_pull))
    public_routes=data['guidance']['GuidanceNodeCollection']
    ourlist=[]
    for i in public_routes:
        if 'preTts' in i:
            ourlist.append(i['preTts'])
    print(ourlist)
    return ourlist

    
    
 



def get_nearest_station(latitude,longitude):
    """
    Given latitude and longitude strings, return a (station_name, wheelchair_accessible, lat, long)
    tuple for the nearest MBTA station to the given coordinates.
    See https://api-v3.mbta.com/docs/swagger/index.html#/Stop/ApiWeb_StopController_index for URL
    formatting requirements for the 'GET /stops' API.
    """
    if longitude>0:
        longitude=-1*longitude
    try:
        mbta_pull=get_json(f'{MBTA_BASE_URL}?api_key={MBTA_API_KEY}&sort=distance&filter%5Blatitude%5D={latitude}&filter%5Blongitude%5D={longitude}')
        station_name=mbta_pull['data'][0]['attributes']['name']
        wheelchair_accessible=mbta_pull['data'][0]['attributes']['wheelchair_boarding']
        lat=mbta_pull['data'][0]['attributes']['latitude']
        long=mbta_pull['data'][0]['attributes']['longitude']
        
        if wheelchair_accessible == 2:
            wheelchair_accessible='not wheelchair accessible'
        elif wheelchair_accessible== 0:
            wheelchair_accessible='unknown'
        else: wheelchair_accessible='wheelchair accessible'
    except IndexError:
        return None
    return station_name,wheelchair_accessible,lat,long
def find_stop_near(place_name):
    """
    Given a place name or address, return the nearest MBTA stop and whether it is wheelchair accessible.
    """
    lat,long=get_lat_long(place_name)
    stop, wheelchair, lat, long=get_nearest_station(lat,long)
    return stop, wheelchair, lat, long
def map_maker(lat, long,w,h, zoom):

    """
    takes lat, long returns api url of map
    """
    return f"https://open.mapquestapi.com/staticmap/v5/map?key={MAPQUEST_API_KEY}&center={lat},{long}&size={w},{h}@2x&zoom={zoom}&locations={lat},{long}"
class MEMES:
    def __init__(self,name,service,location,phonenumber):
        self.name=name
        self.service=service
        self.location=location
        self.phonenumber=phonenumber
        self.distance=None
    def distance_boi(self,current_address):
        lat,long=get_lat_long(self.location)
        clat,clong=get_lat_long(current_address)
        e_distance=((clat-lat)**2+(clong-long)**2)**.5
        self.distance=e_distance
    def __str__(self):
        return self.name
# #overnight ememergency shelters 
# service1=['Southampton Shelter','Overnight shelter (men)','112 Southampton Street, Boston, MA 02118','617-534-5395']
# service2=['Woods Mullen Shelter','Overnight shelter (woman)','794 Massachusetts Ave, Boston, MA 02118','617-534-7100']
# service3=['Pine Street Inn Mens Inn','Overnight shelter (men)','444 Harrison Ave, Boston, MA 02118','617-892-9228']
# service4=['Pine Street Inn Womens Inn','Overnight shelter (women)','363 Albany St, Boston, MA 02118','617-892-9228']
# service5=['Boston Night Center','Overnight drop-in shelter (men and women; no beds)','31 Bowker St, Boston, MA 02114','617-788-1001']
# service6=['New England Center and Home for Veterans','New England Center and Home for Veterans','17 Court St, Boston, MA 02108','617-371-1800']
# service7=['Bridge Over Troubled Waters','Overnight shelter (ages 14-24)','47 West Street, Boston, MA 02111','617-423-9575']
# service8=['Y2Y','Overnight shelter (ages 18-24)','1 Church St Cambridge, MA 02138','617-864-0795']
# service9=['Massachusetts Emergency Family Shelter','Overnight shelter (families)','To apply for shelter services, please call (866) 584-0653 and speak with a Homeless Coordinator.','866-584-0653']
# #daytime sericers and meals
# service10=['City of Boston Office of Food Access','Food resource maps by neighborhood and by language','','617-635-3717']
# service11=['St. Francis House','Meals, daytime shelter and resource center, clothing, showers an toiletries, mail and ID services','39 Boylston Street, Boston, MA 02116','617-542-4211']
# service12=['Boston Warm Day Center, Emmanuel Church (winter)','Day center and meals Mondays and Fridays 9 a.m. - 1 p.m. (September - May)','15 Newbury Street, Boston, MA 02116','']
# service13=['Boston Warm Day Center, Old South Church (summer)','Day center and meals, Thursdays 9 a.m. - 2 p.m. (June - August)','645 Boylston Street Boston, MA 02116','']
# service14=['Rosies Place','Meals and services (women)','889 Harrison Avenue, Boston, MA 02118','617-442-9322']
# service15=['Cardinal Medeiros Day Program','Day shelter and meals, Monday - Friday, 8 a.m. - 3 p.m. (ages 45 and older)','1960 Washington Street, Roxbury, MA 02118','617-619-6960']
# service16=['Womens Lunch Place','Meals, toiletries, showers, laundry, clothes, and day center (women)','67 Newbury Street, Boston, MA 02116','617-267-0200']
# service17=['Bridge Over Troubled Waters','Drop-in day center with meals, shower, lockers, laundry, and case management (ages 14 - 24)','47 West Street, Boston, MA 02111','617-423-9575']
# service18=['Boston Health Care for the Homeless','Medical services','774 Albany St, Boston, MA 02118','857-654-1600']
# #outreach list
# service19=['Boston Police Street Outreach','','','617-343-6478']
# service20=['DMH Homeless Outreach Team','','','617-626-8610']
# service21=['Pine Street Inn (Daytime)','','','617-892-7961']
# service22=['Pine Street Inn (Nighttime)','','','866-633-0170']
# #housing
# service23=['Metrolist','Information on income-restricted and affordable housing opportunities in Boston and neighboring communities','','617-635-4200']
# service24=['HomeStart','Housing search help (walk-in hours, Wednesdays, 3 - 4:30 p.m.)','105 Chauncy Street, Suite 502, Boston, MA 02111','617-542-0338']
# #other list
# service25=['211 / HelpSteps','	Free, multilingual, phone and web-based service with an extensive database of resources','','2-1-1']
# service26=['City of Boston Office of Housing Stability','Tenant and landlord information; help for tenants in housing crisis due to fire, natural disaster, eviction, or condemnation','43 Hawkins Street, Boston, MA 02114','617-635-4200']
# service27=['SafeLink Domestic Violence Hotline','24/7 toll-free domestic violence emergency hotline	','','877-785-2020']
# service28=['Casa Myrna','services for survivors of domestic violence','','877-785-2020']
# service29=['MANNA','Faith community meetings and support by and for those experiencing homelessness','138 Tremont St., Boston, MA 02111','617-482-5800']
# service30=['Project Place','Case management, career services and workforce development','1145 Washington Street, Boston, MA 02118','617-542-3740']
# #for veterans
# service31=['New England Center and Home for Veterans','Shelter, housing, meals, and services','17 Court St, Boston, MA 02108','617-371-1800']
# service32=['City of Boston Veterans services','services and resource connections','43 Hawkins St, 3rd Floor, Boston, MA 02114','617-241-8387']
# service33=['US Department of Veterans Affairs Boston Office','services and resource connections','150 S. Huntington Ave., Jamaica Plain, MA','617-232-9500']
# service34=['Pine Street Inn','Housing and services','444 Harrison Ave, Boston, MA 02118','617-892-9228']
# service35=['Project Place','Case management, career services and workforce development','1145 Washington Street, Boston, MA 02118','617-542-3740']
# #for families
# service36=['Massachusetts Emergency Family Shelter','Overnight shelter (families)','','866-584-0653']
# service37=['FamilyAid Boston','Homelessness prevention and other services for families','3815 Washington Street, Boston, MA 02130','617-542-7286']
# service38=['Home for Little Wanderers','Housing and services for families and youth','10 Guest Street, Boston, MA 02135','617-267-3700']
# resources={
# 'OVERNIGHT EMERGENCY SHELTERS':[service1,service2,service3,service4,service5,service6,service7,service8,service9],
# 'DAYTIME SERVICES AND MEALS':[service10,service11,service12,service13,service14,service15,service16,service17,service18],
# 'OUTREACH SERVICES':[service19,service20,service21,service22],
# 'HOUSING':[service23,service24],
# 'OTHER SERVICES':[service25,service26,service27,service28,service29,service30],
# 'FOR VETERANS':[service31,service32,service33,service34,service34,service35],
# 'FOR FAMILIES':[service36,service37,service38]}


def main():
    """
    You can test all the functions here
    """
    # address_number='7 cedar st'    
    # address_2='wellesley, ma'
    # pprint(property_detailer(address_number,address_2))
    # pprint(postcode(address_number,address_2))
    print(open_guy('25 First St, Cambridge, MA 02141','11 First St, Cambridge, MA 02141'))



if __name__ == '__main__':
    main()



