from gps import *
import time
import requests
import math
import random

TOKEN = "BBFF-6GxdYb8O5TCiz0zxQFlFkiB6oxF2QI"  # Put your TOKEN here
DEVICE_LABEL = "machine"  # Put your device label here 
VARIABLE_LABEL_1 = "temperature"  # Put your first variable label here
VARIABLE_LABEL_2 = "humidity"  # Put your second variable label here
VARIABLE_LABEL_3 = "position"  # Put your second variable label here


def build_payload(variable_1, variable_2, variable_3):

    if nx['class'] == 'TPV':
        latitude = getattr(nx,'lat', "Unknown")
        longitude = getattr(nx,'lon', "Unknown")
        print ("Your position: lon = " + str(longitude) + ", lat = " + str(latitude))

gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)

try:
    print ("Application started!")
    while running:
        getPositionData(gpsd)
        time.sleep(1.0)

    return payload

    def post_request(payload):
        # Creates the headers for the HTTP requests
        url = "http://industrial.api.ubidots.com"
        url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
        headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

        # Makes the HTTP requests
        status = 400
        attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    # Processes results
    print(req.status_code, req.json())
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    print("[INFO] request made properly, your device is updated")
    return True


    def main():
        payload = build_payload(
            VARIABLE_LABEL_1, VARIABLE_LABEL_2, VARIABLE_LABEL_3)

    print("[INFO] Attemping to send data")
    post_request(payload)
    print("[INFO] finished")


    if __name__ == '__main__':
        while (True):
            main()
            time.sleep(1)