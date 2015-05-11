from django.db import models
from django_countries.fields import CountryField
# Create your models here.

class Location(models.Model):
    name = models.FloatField(null=True)
    city = models.FloatField(null=True)
    country = CountryField(null=True)
    lat = models.FloatField()
    lng = models.FloatField()
    google_place_id = models.CharField(max_length=50, null=True)
    foursquare_id = models.CharField(max_length=50, null=True)

    def __repr__(self):
        return unicode("{}, {}, {}".format(self.name, self.city, self.country.name))

class Pics(models.Model):
    image = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    last_updated = models.DateTimeField(auto_now_add=True)
    location = models.ForeignKey("Location", related_name="pictures")
    approved = models.BooleanField(default=False)
    
    def __unicode__(self):
        return unicode(self.image)

    def image_display(self):
        return '<img  src="/media%s" height=120 width=120 />' % self.image
    image_display.allow_tags = True
