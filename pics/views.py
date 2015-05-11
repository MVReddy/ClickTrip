from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from pics.tasks import placeimages
# Create your views here.

class RegisterJob(View):
    def post(self, request, *args, **kwargs):
        try:
            encoding = request.encoding or "utf-8"
            j = json.loads(request.read().decode(encoding))
            #j = json.loads(str(request.body))
            lat = j.get("lat")
            lng = j.get("lng")
            google_place_id = j.get("google_place_id", "").encode()
            if google_place_id:
                google_place_id = bytearray(google_place_id)
            foursquare_id = j.get("foursquare_id", "").encode()
            if foursquare_id:
                foursquare_id = bytearray(foursquare_id)
            placeimages.delay(lat=lat, lng=lng, foursquare_id=foursquare_id, google_place_id=google_place_id)
            return JsonResponse({"status": "success"})
        except ValueError as e:
            return JsonResponse({"error": e})

        
        
        
