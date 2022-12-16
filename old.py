import gps
import time
from ubidots import ApiClient
session = gps.gps("127.0.0.1","2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
api = ApiCLient(token='BBFF-6GxdYb8O5TCiz0zxQFlFkiB6oxF2QI')
variable = api.get_variable('639af3dff560e8000d989e85')

while True:
	try:
		time.sleep(0.5)
		raw_data = session.next()
	if raw_data['class'] == 'TPV':
		if hasattr(raw_data, 'lat') & hasattr (raw_data, 'lon'):
			latitude=raw_data.lat
			longitude=raw_data.lon 
			print "\nLatitude is = "+str(Latitude)
			print "latitude is = "+str(longitude)
			response = variable.save_value({'value':10,
			'context':{'lat': latitude, 'lng': longitude}})
	except KeyError:
		pass
	except KeyboardInterrupt:
		quit()
	except StopIteration:
		session = None
		print "No incoming  data from the GPS module"
