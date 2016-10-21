from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .models import Location
from django.conf import settings
import requests

class LocationAPI(generics.GenericAPIView):
    
    def post(self, request, *args, **kwargs):

        address = request.data.get('address', None)
        print address, "$$$"
        if address:
            headers = {'user-key': settings.ZOMATO_KEY, 'Accept': 'application/json', 'User-agent': 'curl/7.43.0'}
            try:
                r = requests.get(settings.LOCATION_URL, params={'query': address}, headers=headers)
                if r.status_code == 200:
                    result = r.json()
                    if len(result['location_suggestions']) > 0:
                        location_details = result['location_suggestions'][0]
                        entity_type = location_details['entity_type']
                        entity_id = location_details['entity_id']
                        address = location_details['title']
                        lat = location_details['latitude']
                        lon = location_details['longitude']
                        # save in database
                        location_rec,created = Location.objects.get_or_create(entity_type=entity_type,
                                                       entity_id=entity_id,
                                                       address=address,
                                                       lat=lat,
                                                       lon=lon
                                                      )
                        if created:
                            return Response({"status":"1", "location_id":location_rec.pk, "msg": "New record craeted"})
                        elif location_rec:
                            msg = "Record already there"
                            return Response({"status":"1", "location_id":location_rec.pk, "msg":msg})
                    return Response({"status": "0", "msg": "Result Not Found"})
                else:
                    return Response({"status": "0", "msg": "Unexpected API result"})
            except Exception as e:
                print "Exception:", e
                return Response({"status": "0", "msg": "API call failed"})
        else:
            return Response({"status": "0", "msg": "address key is missing"})

