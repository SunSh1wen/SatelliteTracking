from os import name
import numpy as np  
import matplotlib.pylab as plt
from skyfield import api
from pytz import timezone


class Satellite(object):
    def __init__(self, name, tle_name, bluffton, timezone):
        self.name = name
        self.tle_name = tle_name
        self.bluffton = bluffton
        self.url = 'https://celestrak.com/NORAD/elements/'+ tle_name
        self.timezone = timezone

    def sat_dict_gen(self):
        sats = api.load.tle(self.url)
        satellite = sats[self.name]
        return satellite


    def track(self, ts):
        Sat = self.sat_dict_gen()
        difference = Sat - self.bluffton
        topocentric = difference.at(ts)
        alt, az, distance = topocentric.altaz()
        return (alt, az, distance)

    def plot_polar(self, ts):
        alt, az, distance = self.track(ts)
        #print(alt.degrees)
        above_horizon = alt.degrees> 0
        boundaries, = np.diff(above_horizon).nonzero()
        passes = boundaries.reshape(len(boundaries) // 2, 2)


        for i in range(len(passes)):
            m, n = passes[i]
            print('Rises:', ts[m+1].astimezone(self.timezone))
            print('Sets:', ts[n+1].astimezone(self.timezone))
    
            # Set up the polar plot.
            ax = plt.subplot(111, projection='polar')
            ax.set_rlim([90, 0])
            ax.set_theta_zero_location('N')
            ax.set_theta_direction(-1)
    
            # Draw line and labels.
            theta = az.radians
            r = alt.degrees
            ax.plot(theta[m+1:n+1], r[m+1:n+1], 'ro--')
            #for k in range(m+1, n+1):
            #    text = ts[k].astimezone(self.timezone).strftime('%H:%M')
            #    ax.text(theta[k], r[k], text, ha='right', va='bottom')

        plt.show()
            
    def plot_hot(self, ts):
        alt, az, distance = self.track(ts)
        above_horizon = alt.degrees > 0
        indicies, = above_horizon.nonzero()
        boundaries, = np.diff(above_horizon).nonzero()
        passes = boundaries.reshape(len(boundaries) // 2, 2)

        sum = np.zeros(shape =(91,361))

        for i in range(len(passes)):
            m, n = passes[i]
            maxEL = max(alt.degrees[m+1: n+1])
            if maxEL <= 15:
                weight = 1
            elif maxEL <= 30 and maxEL > 15:
                weight = 2
            elif maxEL <= 45 and maxEL > 30:
                weight = 3
            elif maxEL <= 60 and maxEL > 45:
                weight = 4
            else:
                weight = 5

            for j in range(m+1, n+1):
                AZ = round(az.degrees[j]%360)
                EL = round(alt.degrees[j])
                #print(alt.degrees[j])
                sum[EL][AZ] += alt.degrees[j]*weight

            plt.figure("Hot", facecolor="lightgray")
            plt.title("Hot", fontsize=20) 
            plt.xlabel('AZ', fontsize=14)  
            plt.ylabel('EL', fontsize=14)
            plt.tick_params(labelsize=10)  
            plt.grid(linestyle=":")  
            plt.imshow(sum, cmap='jet')

        plt.show()




