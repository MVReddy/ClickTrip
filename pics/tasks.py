from celery import Celery, task
import requests
import cv2
from instagram.client import InstagramAPI
from instagram.bind import InstagramAPIError
import urllib.request
import os
import uuid
import numpy
import sys 

from django.conf import settings
sys.path.insert(0, os.path.join(os.path.abspath(os.path.dirname(__file__)), ".."))
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

from pics.models import Location, Pics
from pics.cel_config import *

app = Celery('tasks', backend="amqp", broker='amqp://127.0.0.1')

@task(name="pics.tasks.placeimage")
def placeimages(lat=None, lng=None, foursquare_id=None, google_place_id=None):
    location = Location.objects.create(lat=lat, lng=lng)
    urls = fetch_instagram(INSTAGRAM_CLIENT_ID, 
                             INSTAGRAM_CLIENT_SECRET,
                             lat=lat,
                             lng=lng, 
                             foursquare_id=foursquare_id)
    
    urls = sizefilter(urls)
    images = apply_filters(urls)
    for src, img in images:
        Pics.objects.create(
            image = img,
            source = src,
            location = location
        )
    return images
    
def sizefilter(urls):
    images = []
    for url, w, h in urls:
        if h >= 600 and w >=600 and not (h-w) > 1 and not (w-h) > 1:
            images.append((url,w, h))
    return images

def get_all_images(urls):
    images = []
    for url, w, h in urls: 
        suffix=url.split(".")[-1]
        filename = os.path.join("/tmp", str(uuid.uuid4()) + "." + suffix)
        filename, r = urllib.request.urlretrieve(url, filename)
        images.append((url, filename))
    return images

def facefilter(images):
    face_cascade = cv2.CascadeClassifier('/usr/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml')
    profile_face_cascade = cv2.CascadeClassifier('/usr/share/OpenCV/haarcascades/haarcascade_profileface.xml')
    fullbody_cascade = cv2.CascadeClassifier('/usr/share/OpenCV/haarcascades/haarcascade_fullbody.xml')
    #upperbody_cascade = cv2.CascadeClassifier('/usr/share/OpenCV/haarcascades/haarcascade_upperbody.xml')
    eye_cascade = cv2.CascadeClassifier('/usr/share/OpenCV/haarcascades/haarcascade_eye.xml')

    #apply only required cascades
    cascades = [face_cascade, profile_face_cascade, eye_cascade] #fullbody_cascade, upperbody_cascade]

    for url, img in images:
        i = cv2.imread(img)
        gray = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)
        
        for cas in cascades:
            faces = cas.detectMultiScale(gray, 1.3, 5)
            if numpy.array(faces).any():
                images = [(src, f) for src, f in images if f != img]
                os.remove(img)
                break
    return images
            
def apply_filters(urls):
    filters = [facefilter,]
    images = get_all_images(urls)
    for fil in filters:
        images = fil(images)
    return images
    

#1. get json response of the place from google places, foursquare, instagram
#2. extract image links
#3. fetch all images 

def fetch_instagram(client_id, client_secret, lat=None, lng=None, foursquare_id=None):
    api = InstagramAPI(client_id=client_id, client_secret=client_secret)
    try:
        l = api.location_search(lat=lat, lng=lng, foursquare_v2_id=foursquare_id)
        ids = [o.id for o in l]
        images=[]
        for lid in ids:
            i, _ = api.location_recent_media(location_id=lid)
            for img in i:
                pic = img.images['standard_resolution']
                images.append((pic.url, pic.width, pic.height))
        return images
    except InstagramAPIError as e:
        return []

def fetch_foursquare(client_id, client_secret, foursquare_id):
    client = foursquare.Foursquare(client_id=FOURSQUARE_CLIENT_ID, client_secret=FOURSQUARE_SECRET_ID)
    r = client.venues(foursquare_id)
    
