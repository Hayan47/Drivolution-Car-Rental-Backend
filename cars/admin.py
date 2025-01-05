from django.contrib import admin
from .models import Car, CarImage, Location

# admin.site.register(Car)
admin.site.register(CarImage)
admin.site.register(Location)


class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    inlines = [CarImageInline]
