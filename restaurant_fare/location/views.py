from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .models import Location
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
import requests

class LocationAPI(generics.GenericAPIView):
    
    def post(self, request, *args, **kwargs):

        address = request.data.get('address', None)

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


class FareAPI(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):

        location_id = kwargs.get('lid')
        if location_id:
            try:
                location = Location.objects.get(pk=location_id)
                # call best restaurant API
                headers = {'user-key': settings.ZOMATO_KEY, 'Accept': 'application/json', 'User-agent': 'curl/7.43.0'}
                r = requests.get(settings.LOCATION_DETAILS_URL,
                                 params={'entity_type': location.entity_type,
                                         'entity_id': location.entity_id
                                        },
                                 headers=headers
                                 )
                res_result = r.json()

                # output list to return having info about restaurant, its rating and fare to reach
                res_rating_fare = []

                start_latitiude = location.lat
                start_longituide = location.lon
                uber_headers = headers = {'Authorization': 'Token '+settings.UBER_TOKEN, 'Accept': 'application/json', 'User-agent': 'curl/7.43.0'}
                tot_res_to_iterate = min(res_result['num_restaurant'], 10)
                for best_res in res_result['best_rated_restaurant'][0:tot_res_to_iterate]:
                    end_latitude = best_res['restaurant']['location']['latitude']
                    end_longitude = best_res['restaurant']['location']['longitude']

                    # call uber API
                    r = requests.get(settings.UBER_FARE_URL,
                                 params={'start_latitude': start_latitiude,
                                         'start_longitude': start_longituide,
                                         'end_latitude': end_latitude,
                                         'end_longitude': end_longitude
                                        },
                                 headers=headers
                                 )
                    #print r.json()
                    uber_res = r.json()
                    res_rating_fare.append({
                                            "name": best_res['restaurant']['name'],
                                            "rating": best_res['restaurant']['user_rating']['aggregate_rating'],
                                            "uber_fare": [{"service": u['localized_display_name'], "fare": u['low_estimate']} for u in uber_res['prices']]
                                           })

                #print res_rating_fare

            except ObjectDoesNotExist:
                return Response({"status": "0", "msg": "Location record not found"})
            except Exception as e:
                return Response({"status": "0", "msg": "Exception:"+str(e)})
            return Response({"status": "1", "restaurant_fare": res_rating_fare})
        else:
            return Response({"status": "0", "msg": "location id not provided"})
