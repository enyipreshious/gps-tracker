from gps import *
import time
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
gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)

def getPositionData(gps):
    nx = gpsd.next()
    if nx['class'] == 'TPV':
        latitude = getattr(nx,'lat', 0)
        longitude = getattr(nx,'lon', 0)
        print ("Your position: lon = " + str(longitude) + ", lat = " + str(latitude))
        return latitude, longitude

try:
    print ("Application started!")
    while RUNNING:
        position = getPositionData(gpsd)
        if (position):
            gps_variable.save_value({"value": 0, "context": { "lat": position[0], "lng": position[1]}})
        time.sleep(0.1)

except (KeyboardInterrupt):
    RUNNING = False
    print ("Applications closed!")
