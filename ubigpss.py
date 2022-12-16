from gps import *
import time
from ubidots import ApiClient

api = ApiClient(token='BBFF-6GxdYb8O5TCiz0zxQFlFkiB6oxF2QI')
variable = api.get_variable('639b5c86f61c66000ed690a5')
running = True

def getPositionData(gps):
    nx = gpsd.next()
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

except (KeyboardInterrupt):
    running = False
    print ("Applications closed!")