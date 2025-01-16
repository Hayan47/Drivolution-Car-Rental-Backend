from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from cars.models import Car
from django.core.cache import cache


@receiver([post_save, post_delete], sender=Car)
def invalidate_cars_cache(sender, instance, **kwargs):
    """
    Invalidates cars list caches when a car is created, updated or deleted
    """
    print("Clearing Cars Cache")
    cache.delete_pattern("*cars_list*")
