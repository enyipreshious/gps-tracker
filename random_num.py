import random
import time
from ubidots import ApiClient

api = ApiClient(token='BBFF-6GxdYb8O5TCiz0zxQFlFkiB6oxF2QI')
variable = api.get_variable('639b636f00f9fe000b0348bf')
while(1):
    x=random.randint(1,100)
    response = variable.save_value({"value":x})
    print ("\nThe random number sent to IoT dashboard is "+str(x))
    time.sleep(0.1)
