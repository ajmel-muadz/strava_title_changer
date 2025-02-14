import requests
from pprint import pprint
from datetime import datetime, timezone
import time

ACCESS_TOKEN = "REDACTED"

original_dict = {}
sorted_dict = {}  # Sorted by dates as keys with associated ID's

# This is all the GET request for every single activity. We get all activities and store in dictionary.
# ----------------------------------------------------------------------------------- #
num = 0
for i in range(4, 0, -1):
    read_url = f"https://www.strava.com/api/v3/athlete/activities?page={i}&per_page=100"
    read_headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

    try:
        response = requests.get(read_url, headers=read_headers)
        json = response.json()
        for element in json:
            num += 1
            original_dict[element["id"]] = element["start_date"]

    except requests.exceptions.HTTPError as e:
        print(f"An error occurred: {e}")
    except requests.exceptions.ConnectionError as e:
        print(f"An error occurred: {e}")
# ----------------------------------------------------------------------------------- #

# Now that we got all the data we need to re-order them. We do this by re-ordering using date.
# Before re-ordering however, we must convert string dates into datetime objects.
# We also put datetime objects as keys paired with activity IDs, so that ordering of activities
# would be possible.
print(num)
for id_value, string_date in original_dict.items():
    date_object = datetime.fromisoformat(string_date.replace("Z", "+00:00"))
    sorted_dict[date_object] = id_value

# Now it's time to actually sort the dates. They are now datetime objects.
# Credits to Aalok Kumar on this link: https://stackoverflow.com/questions/34129391/sort-python-dictionary-by-date-key
sorted_dict = sorted(sorted_dict.items())
sorted_dict = dict(sorted_dict)

# This is all the PUT request for every activity. Simply rename activities into this format: #{number of activity}
# ------------------------------------------------------------------------------------------ #
activity_num = 1
for date_object, id_value in sorted_dict.items():
    url_2 = f"https://www.strava.com/api/v3/activities/{id_value}"
    headers_2 = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

    try:
        new_name = f"#{str(activity_num)}"
        put = requests.put(url_2, {"name": new_name}, headers=headers_2)

        if put.status_code == 200:
            print(f"Successfully updated activity {id_value} to {new_name}")
        else:
            print(f"Failed to update activity {id_value}. Status code: {put.status_code}.")

        time.sleep(6) # Sleep for 6 seconds to ensure we don't overwhelm the server.
        
        activity_num += 1

    except requests.exceptions.HTTPError as e:
        print(f"An error occurred: {e}")
    except requests.exceptions.ConnectionError as e:
        print(f"An error occurred: {e}")
# ------------------------------------------------------------------------------------------ #
