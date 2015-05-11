import urllib.urlencode
import requests

class GooglePlaces:
    
    def __init__(self, api_key):
        self.api_key = api_key
        
    def places_reference(self, place_id):
        url = 'https://maps.googleapis.com/maps/api/place/details/json?{}'
        r = request.get(url.format(urllib.parse.encode({'placeid': place_id, 'key':self.api_key})))
        if r.status_code == 200:
            j = r.json()
            return j['reference']
        return None

    def photos(self, photoreference):
        url = 'https://maps.googleapis.com/maps/api/place/photo?{}'
        params = {'photoreference': photoreference, 'key': self.api_key, 'maxwidth': 600, 'maxheight': 600}
        return url.format(urllib.parse.encode(params)
