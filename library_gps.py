from gps import *
import time
import requests

running = True

TOKEN = "BBFF-YWXadsPJMVdAciZYPRb7aRZLtVYgjG"
DEVICE_LABEL = "rasp"  # Put your device label here 
def getPositionData(gps):
    nx = gpsd.next()
    # For a list of all supported classes and fields refer to:
    # https://gpsd.gitlab.io/gpsd/gpsd_json.html
    if nx['class'] == 'TPV':
        latitude = getattr(nx,'lat', 0)
        longitude = getattr(nx,'lon', 0)
        print ("Your position: lon = " + str(longitude) + ", lat = " + str(latitude))
        return latitude, longitude

gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)

def post_request(payload):
    print("[INFO] Sending data to ubidots")
    # Creates the headers for the HTTP requests
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    print(payload)
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    # Processes results
    print(req.status_code, req.json())
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check your token credentials and internet connection")
        return False

    print("[INFO] request made properly, your device is updated")
    return True

try:
    print ("Application started!")
    while running:
        position = getPositionData(gpsd)
        if (position):
            post_request({
                "gps": {
                    "value": 1,
                    "context": {
                        "lat": position[0], # latitude
                        "lng": position[1] # longitude
                    }
                }
            })
        time.sleep(1.0)

except (KeyboardInterrupt):
    running = False
    print ("Applications closed!")
