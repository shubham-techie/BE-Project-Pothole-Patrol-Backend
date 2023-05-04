"""
We get geo_coordinates for each pothole report from user or traffic camera videos. 
So, while saving these in DB, we are fetching "state" from which pothole report came using "geopy" API.
And that same string value of state is to be stored in "StateRoadAuthority" table as well because we will be
sending that report to particular road safety authority of that state.

Therfore, for populating "StateRoadAuthority" table with same state value as "PotholeDetails" table, 
we are getting "state" from same "geopy" API, so that we don't get any errors.

"""

from geopy.geocoders import Nominatim
import pandas as pd
import os
import csv
import django
from django.db import transaction

class Populate_StateRoadAuthority_Table:
    def __init__(self) -> None:
        self.text_file_name = "utility/geopy_states.txt"
        self.csv_file_name = "utility/state_road_authority_email.csv"

    def get_geopy_states(self):
        states = ["Andhra Pradesh","Arunachal Pradesh ","Assam","Bihar","Chhattisgarh","Goa","Gujarat","Haryana","Himachal Pradesh","Jammu and Kashmir","Jharkhand","Karnataka","Kerala","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal","Andaman and Nicobar Islands","Chandigarh","Dadra and Nagar Haveli","Daman and Diu","Lakshadweep","National Capital Territory of Delhi","Puducherry"]
        geopy_states = []
        gc = Nominatim(user_agent="pothole_patrol")

        for state in states:
            new_state = gc.geocode(state).address.split(',')[0]
            geopy_states.append(new_state)
            print(f'{state} --------> {new_state}')
        
        print(geopy_states)
        with open(self.text_file_name,"w+") as f:
            f.write(str(geopy_states))
            print("file saved.")
        
        
    def create_dummy_email_for_state(self):
        geopy_states = []
        with open(self.text_file_name, "r") as f:
            geopy_states = eval(f.readline())
        print(geopy_states)

        df = pd.DataFrame({"state" : geopy_states})
        def process_email(row):
            state = row['state'].split(' ')
            state = ''.join(state).lower()
            email = f'roadsafety.{state}@gmail.com'
            return email

        df['email'] = df.apply(process_email, axis=1)
        print(df)    
        df.to_csv(self.csv_file_name, index=False)
        print("csv file created.")

    
    def run_populate(self):
        with transaction.atomic():
            with open(self.csv_file_name, 'r') as csv_file:
                reader = csv.reader(csv_file)             
                for i, row in enumerate(reader):
                    if i:
                        obj = StateRoadAuthority(state=row[0], email=row[1])
                        obj.save()
                        print(i, " object saved.")
                

if __name__ == "__main__":
    import sys
    sys.path.append(".")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pothole_patrol_backend.settings')
    django.setup()

    from road_damage_notifyapi.models import StateRoadAuthority

    if not StateRoadAuthority.objects.all().count():
        fill_db = Populate_StateRoadAuthority_Table()

        if not os.path.isfile(fill_db.text_file_name):
            fill_db.get_geopy_states()

        if not os.path.isfile(fill_db.csv_file_name):
            fill_db.create_dummy_email_for_state()

        fill_db.run_populate()

    else:
        print("Objects are already present.")
