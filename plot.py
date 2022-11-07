import numpy as np  
import matplotlib.pylab as plt
import matplotlib.pylab as mp
from skyfield import api
from pytz import timezone
from Satellite import Satellite 


beijing = timezone('Asia/Shanghai')
#sats = api.load.tle('https://celestrak.com/NORAD/elements/stations.txt')

half_minutes = range(0, 10 * 24 * 60 * 60, 30)
t = api.load.timescale()
ts = t.utc(2022, 9, 22, 16, 0, half_minutes)
bluffton = api.Topos(latitude='39.99 N', longitude='116.76 E')

Sat = Satellite('CSS (TIANHE)', 'stations.txt', bluffton, beijing )

Sat.plot_polar(ts)
Sat.plot_hot(ts)