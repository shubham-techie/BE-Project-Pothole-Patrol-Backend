from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import PotholeReport
from geopy.geocoders import Nominatim
from road_damage_notifyapi.models import StateRoadAuthority
from utility.utils import send_email
from django.conf import settings


@receiver(pre_save, sender=PotholeReport)
def fetch_and_save_state(sender, instance, **kwargs):
    longitude = instance.geo_location.x
    latitude = instance.geo_location.y

    geocoder = Nominatim(user_agent = 'pothole_patrol')
    location = geocoder.reverse((latitude, longitude))
    
    if location is not None:
        address = location.raw['address']
        instance.state = address.get('state')


@receiver(post_save, sender=PotholeReport)
def report_road_authority(sender, instance, created, **kwargs):
    if created:
        if not StateRoadAuthority.objects.all().count():
            print("first populate the state authority email ids.")
            return
        
        state = instance.state
        longitude = instance.geo_location.x
        latitude = instance.geo_location.y

        if state:
            try:
                state_road_authority = StateRoadAuthority.objects.get(state=state)
                authority_email = state_road_authority.email
            except:
                print(f"Pothole coordinates is from outside India. It is from {state}. Hence, mail cannot be send.")
            else:
                send_email(to=authority_email,
                        authority=True,
                        state=state, 
                        latitude=latitude, 
                        longitude=longitude
                        )
                send_email(to=instance.user.email,
                        username=instance.user.username,
                        state=state, 
                        latitude=latitude, 
                        longitude=longitude
                        )
                print(f"pothole issue has been reported to {state} road authority.")
        else:
            print("State is not fetched for given coordinates. Hence, mail cannot be send.")
    else:
        print("pothole coordinates has not been saved.")
