# NOTE: strava_organiser_2.py is just a lazy way to fix any activities that failed to update its
# name from strava_organiser.py (the original file to use).
import requests
import time

ACTIVITY_NUMBER_INDEX = 4
STARTING_NUMBER = 97
ACCESS_TOKEN = "REDACTED"

failed_activities_file = open("failed_activities.txt", "r")

# This part is responsible for parsing activity numbers into numbers.
list_of_activities = []
for line in failed_activities_file:
    split_line = line.split(" ")
    activity_number = split_line[ACTIVITY_NUMBER_INDEX]
    activity_number = activity_number.replace(".", "")
    activity_number = int(activity_number)
    list_of_activities.append(activity_number)

# Responsible for updating the activities
for id_value in list_of_activities:
    url = f"https://www.strava.com/api/v3/activities/{STARTING_NUMBER}"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

    try:
        new_name = f"#{str(STARTING_NUMBER)}"
        put = requests.put(url, {"name": new_name}, headers=headers)

        if put.status_code == 200:
            print(f"Successfully updated activity {id_value} to {new_name}")
        else:
            print(f"Failed to update activity {id_value}. Status code: {put.status_code}.")

        time.sleep(10) # Sleep for 6 seconds to ensure we don't overwhelm the server.
    except requests.exceptions.HTTPError as e:
        print(f"An error occurred: {e}")
    except requests.exceptions.ConnectionError as e:
        print(f"An error occurred: {e}")
    
    STARTING_NUMBER += 1