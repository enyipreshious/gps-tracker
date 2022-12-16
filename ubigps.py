from gps import *
import time
from ubidots import ApiClient
def getPositionData(gps):
    nx = gpsd.next()
    if nx['class'] == 'TPV':
        latitude = getattr(nx,'lat', "Unknown")
        longitude = getattr(nx,'lon', "Unknown")
        print ("Your position: lon = " + str(longitude) + ", lat = " + str(latitude))
gpsd = gps (mode=WATCH_ENABLE|WATCH_NEWSTYLE)
api = ApiClient(token='BBFF-6GxdYb8O5TCiz0zxQFlFkiB6oxF2QI')
variable = api.get_variable('639af3dff560e8000d989e85')
 
while True:
    try:
        time.sleep(0.5)
            if hasattr(raw_data, 'lat')& hasattr(raw_data, 'lon'):
                latitude=raw_data.lat
                longitude=raw_data.lon
                print("\nLatitude is = "+str(latitude))
                print("Latitude is = "+str(longitude))
                response = variable.save_value({'value':10, 'context':{'lat': latitude,'lng': longitude}})
    except KeyError:
        pass
    except KeyboardInterrupt:
        quit()
    except StopIteration:
        session = None
        print("No incoming data from the GPS module")

