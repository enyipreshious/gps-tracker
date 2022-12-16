import requests
import time
from math import *

TOKEN = 'BBFF-6GxdYb8O5TCiz0zxQFlFkiB6oxF2QI'  # Assign your Ubidots TOKEN
DEVICE_LABEL = 'iss'  # Assign the device label desired
VARIABLE_LABEL = "distance"

BASE_URL = 'http://industrial.api.ubidots.com/api/v1.6/devices/'

# Assign your home coordinates
LAT_HOME = 5.440623717400113
LNG_HOME = 7.077475343127787


def get_iss_position():
    # Get current ISS position
    req_iss = requests.get('http://api.open-notify.org/iss-now.json')
    dict = req_iss.json()
    lat_lng = dict['iss_position']
    # save the current ISS  possition in new variables
    lat_iss = float(lat_lng['latitude'])
    lng_iss = float(lat_lng['longitude'])
    return lat_iss, lng_iss


def deg2rad(deg):
    return deg * (pi/180)


def getDistance(lat_iss, lng_iss, lat_home, lng_home):
    R = 6371  # Radius of the earth in km
    dLat = deg2rad(lat_home-lat_iss)  # deg2rad below
    dLng = deg2rad(lng_home-lng_iss)
    a = sin(dLat/2) * sin(dLat/2) + cos(deg2rad(lat_iss)) * \
        cos(deg2rad(lat_home)) * sin(dLng/2) * sin(dLng/2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    d = R * c  # Distance in km to Home
    return d


def build_payload(variable_label, value, lat_iss, lng_iss):
    # Build the payload to be sent
    payload = {variable_label: value, "position": {
        "value": 1, "context": {"lat": lat_iss, "lng": lng_iss}}}
    return payload


def send_ubidots(device_label, payload):
    # Make the HTTP request to Ubidots
    url = "{0}{1}/?token={2}".format(BASE_URL, device_label, TOKEN)
    status = 400
    attempts = 0

    while status >= 400 and attempts <= 5:
        req = requests.post(url, json=payload)
        status = req.status_code
        attempts += 1

    response = req.json()

    return response


def main(device_label, variable_label, lat_home, lng_home):
    # Get the current ISS position
    lat_iss, lng_iss = get_iss_position()
    # Caculate the distance in KM to Home
    distance = getDistance(lat_iss, lng_iss, lat_home, lng_home)
    distance = round(distance, 1)
    # Build the payload to be sent
    payload = build_payload(variable_label, distance, lat_iss, lng_iss)
    # Send the HTTP request to Ubidots
    response = send_ubidots(device_label, payload)

    return response


if __name__ == '__main__':
    while True:
        try:
            response = main(DEVICE_LABEL, VARIABLE_LABEL, LAT_HOME, LNG_HOME)
            print("response json from server: \n{0}".format(response))
        except:
            pass

        time.sleep(1)
