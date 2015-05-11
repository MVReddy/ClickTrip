from django.contrib import admin

# Register your models here.

from pics.models import Location, Pics

class LocationAdmin(admin.ModelAdmin):
    pass
admin.site.register(Location, LocationAdmin)

class PicsAdmin(admin.ModelAdmin):
    list_display = ("location", "image_display", "approved")

admin.site.register(Pics, PicsAdmin)
