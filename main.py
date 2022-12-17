import os
import time
import gpsd
import requests
from ubidots import ApiClient
from dotenv import load_dotenv

load_dotenv()

RUNNING = True
TOKEN = os.getenv("UBIDOTS_TOKEN")
VARIABLES = {
    "gps": os.getenv("UBIDOTS_VARIABLE_GPS")
}
api = ApiClient(token=TOKEN)
gps_variable = api.get_variable(VARIABLES["gps"])
gpsd.connect()

def getPositionData():
    packet = gpsd.get_current()
    latitude, longitude = packet.position()
    print ("Your position: lon = " + str(longitude) + ", lat = " + str(latitude))
    return latitude, longitude

if __name__ == "__main__":
    try:
        print ("Application started!")
        while RUNNING:
            try:
                position = getPositionData()
                if (position):
                    if not (position[0] == 0 and position[1] == 0):
                        gps_variable.save_value({"value": 0, "context": { "lat": position[0], "lng": position[1]}})
            except gpsd.NoFixError:
                print("Try re-positioning GPS")
                
            time.sleep(0.1)

    except (KeyboardInterrupt):
        RUNNING = False
        print ("Applications closed!")
