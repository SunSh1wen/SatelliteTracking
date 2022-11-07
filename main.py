import time
from pytz import timezone
from skyfield.api import load, wgs84
from Satellite import Satellite 
from udp_server import rotate_to_degree, get_degree, rotator_stop, turn_left, turn_right, turn_up, turn_down

ts = load.timescale()

# set location
lat = 39.99 
lon = 116.76
alt_de = 20  
elevation = 52  
bluffton = wgs84.latlon(lat, lon, elevation_m=elevation)
# observer location

beijing = timezone('Asia/Shanghai')
Sat = Satellite('CSS (TIANHE)', 'stations.txt', bluffton, beijing)
 
while True:
    try:

        #get degree of Satellite
        El_degree, Az_degree, distance = Sat.track(ts.now())
        print('[Set Position to] AZ=',Az_degree,' EL=',El_degree)


        #get degree of Rotator 
        hori = get_degree(1)
        vert = 90-get_degree(1, False)
        print('[Get Position] AZ=',hori,' EL=',vert)
        time.sleep(0.05)

        #rotate to degree
        if abs(Az_degree- hori)>= 0.5 or abs(El_degree- vert)>= 0.25:
            rotate_to_degree(1, Az_degree)
            rotate_to_degree(1, 90-El_degree, 0)
        else:
            rotator_stop()

        time.sleep(0.45)
    except KeyboardInterrupt:
        print("---------------[Ctrl+C Pressed]---------------")
        break


rotate_to_degree(1, 0)
rotate_to_degree(1, 0, 0)
print('[Back to Zero]')

