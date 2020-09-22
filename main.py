import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from MPLP import *
import random
import os 

################################################################################
# begining of class
################################################################################

class PyGlobe:

    def __init__(self):
        """
        class initaliser
        """
        print('#'*55)
        print(' PyGlobe initalised '+self.get_live_time())
        print('#'*55)

    ######################################################################################
    
    def spherical_to_cartesian(self,theta,phi,radius):
        """
        simple spherical to cartesian coord transform
        """
        x = radius * np.sin(theta) * np.cos(phi)
        y = radius * np.sin(theta) * np.sin(phi)
        z = radius * np.cos(theta)

        return x,y,z

    ######################################################################################
    
    def degrees_to_radians(self,angle):
        """
        degrees to radians angle converter
        """
        angle = float(angle/180)*np.pi
        return angle

    ######################################################################################
    
    def cartesian_transformation_radial(self,x,y,z,orbit_radius,orbital_inclination,angluar_orbital_position):
        """
        orbiatal position and inclination transformations
        """
        orbital_inclination = self.degrees_to_radians(orbital_inclination)

        x = x + orbit_radius*np.cos(angluar_orbital_position)
        y = y + orbit_radius*np.sin(angluar_orbital_position)
        z = z
        return x,y,z

    ######################################################################################
    
    def cartesian_transformation_obliquity(self,x,y,z,obliquity):
        """
        converts cartesian coords to cartesian coords with a obliquity tilt 
        """
        obliquity = self.degrees_to_radians(-obliquity)
        z =  z*np.cos(obliquity) + x*np.sin(obliquity)
        x = -z*np.sin(obliquity) + x*np.cos(obliquity)
        return x,y,z

    ######################################################################################
    
    def coordinate_selector(self,ax,input_longitude,input_latitude):
        """
        will indicate a point on earth with a point plotted on the globe
        """
        orbital_inclination = self.degrees_to_radians(23.5)
        body_radius = 6378 #km for earth

        longitude = self.degrees_to_radians(input_longitude + 180)
        latitude  = self.degrees_to_radians(input_latitude)

        x,y,z    = self.spherical_to_cartesian(latitude,longitude,body_radius+1)
        dx,dy,dz = self.spherical_to_cartesian(latitude,longitude,body_radius + 10000)

        ax.plot([x,dx],[y,dy],[z,dz],c='r')
        print(' - Cordinate beam generated [{},{}]'.format(input_longitude,input_latitude))

    ######################################################################################
    
    def plot_orbit(self,ax,colour,orbit_radius,orbital_inclination):
        """
        plots a bodies orbital path
        """
        orbital_inclination = self.degrees_to_radians(orbital_inclination)

        x_data = []
        y_data = []
        z_data = []
        
        theta = 2*np.pi/100
        
        for i in range(100+1):
            x_orb = orbit_radius*np.cos(theta * i)
            y_orb = orbit_radius*np.sin(theta * i)
            z_orb = x_orb * np.sin(orbital_inclination)
            
            x_data.append(x_orb)
            y_data.append(y_orb)
            z_data.append(z_orb)
                
        ax.plot(x_data,y_data,z_data,color=colour,linewidth=1,linestyle='--')
 
    ######################################################################################
    
    def calculate_position_and_orientation(self,date,hour,orbit_radius,obliquity,orbit_duration_days):
        """
        calculates the orbital position of a body given a date
        """

        #currently centered around earth
        
        day = int(date.split('/')[0])
        
        # to be made correct 
        angluar_orbital_position = (float(day+(hour/24.))/orbit_duration_days)*np.pi*2

        # to be made correct should always face earth
        obliquity = obliquity

        #to be made elliptical
        orbit_radius=orbit_radius

        return orbit_radius,obliquity,angluar_orbital_position

    ######################################################################################

    def spherical_body(self,ax,date,hour,name,image_file,body_radius,obliquity,orbit_radius,orbital_inclination,rotation_duration_hrs,orbit_duration_days):
        """
        generates a rendered spherical body
        """

        
        img = plt.imread(image_file)

        # define a grid matching the map size, subsample along with pixel    
        theta = np.linspace(0, np.pi, img.shape[0])
        if name == 'Earth':
            rot   = float(2*np.pi*hour/rotation_duration_hrs)

        if name == 'Moon':
            day = int(date.split('/')[0])
            rot   = float(2*np.pi*(int(day)*24+hour)/rotation_duration_hrs)

        phi   = np.linspace(0+rot, 2*np.pi+rot, img.shape[1])

        count = 180 # keep 180 points along theta and phi

        theta_inds = np.linspace(0, img.shape[0] - 1, count).round().astype(int)
        phi_inds   = np.linspace(0, img.shape[1] - 1, count).round().astype(int)

        theta = theta[theta_inds]
        phi   = phi[phi_inds]

        img = img[np.ix_(theta_inds, phi_inds)]

        theta,phi = np.meshgrid(theta, phi)
        
        # transformations
        #spherical
        x,y,z = self.spherical_to_cartesian(theta,phi,body_radius)
        #body tilt
        x,y,z = self.cartesian_transformation_obliquity(x,y,z,obliquity)
        

        if orbit_radius != 0:
            orbit_radius,obliquity,angluar_orbital_position=self.calculate_position_and_orientation(date,hour,orbit_radius,obliquity,orbit_duration_days)
            self.plot_orbit(ax,'grey',orbit_radius,orbital_inclination)
            #orbital position
            x,y,z = self.cartesian_transformation_radial(x,y,z,orbit_radius,orbital_inclination,angluar_orbital_position)
    

        ax.plot_surface(x.T, y.T, z.T, facecolors=img/255, cstride=1, rstride=1)
        print(' - {} generated.'.format(name))

    ######################################################################################
    
    def starry_night(self,ax,max_lim,num_of_Stars):
        """
        plots random stars in foreground and background
        """

        random.seed(1)
        
        ax.set_facecolor('black')
        
        ax.w_xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
        ax.w_yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
        ax.w_zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
        
        x1 = []
        x2 = []
        x3 = []
        
        min_lim = -max_lim
        
        s = random.randrange(start=1, stop=3)
        
        for i in range(int(num_of_Stars/6)):
            x1.append(random.randrange(start=min_lim, stop=max_lim))
            x2.append(random.randrange(start=min_lim, stop=max_lim))
            x3.append(min_lim)
        
        ax.scatter(x1, x2, x3, c='white', s=s)
        ax.scatter(x2, x3, x1, c='white', s=s)
        ax.scatter(x3, x1, x2, c='white', s=s)
        
        for i in range(int(num_of_Stars/6)):
            x1.append(random.randrange(start=min_lim, stop=max_lim))
            x2.append(random.randrange(start=min_lim, stop=max_lim))
            x3.append(max_lim)
        
        ax.scatter(x1, x2, x3, c='white', s=s)
        ax.scatter(x2, x3, x1, c='white', s=s)
        ax.scatter(x3, x1, x2, c='white', s=s)
        print(' - Stars generated.')

    ######################################################################################
    
    def get_live_time(self):
        """
        returns live time and date for uk
        """
        date     = str(os.popen("date +%D").readlines())[2:-4]
        time     = str(os.popen("date +%T").readlines())[2:-7]
        timezone = str(os.popen("date +%:z").readlines())[2:-7]

        live = time + ' ' + timezone + ' ' + date
        return live

    ######################################################################################

    def plot(self,date,hour,coord_selector,show):       
        """
        plots eath moon system given a date eg 01/01/2000
        """

        if date=='live':
            date=(self.get_live_time().split(' ')[-1])

        if hour =='live':
            hour=int((self.get_live_time().split(' ')[0]).split(':')[0])

        print('{}:00 {}'.format(hour,date))

        fig = plt.figure('Globe '+ date)
        ax = fig.add_subplot(111, projection='3d')

        #set axis lims
        max_lim =  8000
        min_lim = -max_lim
        
        ax.set_xlim3d([min_lim,max_lim])
        ax.set_xlabel('km')
        
        ax.set_ylim3d([min_lim,max_lim])
        ax.set_ylabel('km')
        
        ax.set_zlim3d([min_lim,max_lim])
        ax.set_zlabel('km')

        ######################################################################################
        # Space
        star_distance   = max_lim*7
        number_of_stars = 6000
        self.starry_night(ax,star_distance,number_of_stars)

        #use Equirectangular projections for img files

        ######################################################################################
        # Earth

        name                  = 'Earth'
        img                   = 'surfaces/earth.jpg'
        body_radius           = 6378 #km
        radial_position       = 0 #km
        obliquity             = 23.5 #degs
        orbital_inclination   = 0 #degs
        rotation_duration_hrs = 24
        orbit_duration_days   = 0
        self.spherical_body(ax,date,hour,name,img,body_radius,obliquity,radial_position,orbital_inclination,rotation_duration_hrs,orbit_duration_days)

        ######################################################################################
        # Moon

        name                  = 'Moon'
        img                   = 'surfaces/moon.jpg'
        body_radius           = 1737.5 #km
        radial_position       = 12000 #km (should be 384000)
        obliquity             = -6.7 #degs
        orbital_inclination   = 5 #degs
        rotation_duration_hrs = 28*24
        orbit_duration_days   = 28
        self.spherical_body(ax,date,hour,name,img,body_radius,obliquity,radial_position,orbital_inclination,rotation_duration_hrs,orbit_duration_days)

        ######################################################################################

        if coord_selector != None:
            self.coordinate_selector(ax,0,0) #currently on renders behind a sphere

        MPL_Prefs(fig,ax,'','no_grid')

        if show != None:
            plt.show()

################################################################################
# End of class
################################################################################

def make_gif():
    """
    generates screenshots of the program across a 28 days and then compiles them into a gif
    """
    g = PyGlobe()

    # every day date in a 28 cycle in 1 day incriments
    for day in range(1,28,1):
        date = "{}/08/2020".format(day)

        # every hour in 6 hour incriments
        for hour in range(0,24,4):
            g.plot(date,hour,None,None)

            if len(str(hour)) == 1:
                hour = str('0{}'.format(hour))

            if len(str(day)) == 1:
                date = "0{}/08/2020".format(day)

            filename = 'Images/progression/{}_{}-00.png'.format(date.replace('/','-'),hour)
            plt.savefig(filename)
            print(' - Image saved')

    # convert all saved images to a single gif
    import imageio
    images = []
    for filename in os.listdir('Images/progression/'):
        images.append(imageio.imread('Images/progression/'+filename))
    imageio.mimsave('Images/lunar.gif', images)
    print('gif made')

################################################################################

#make_gif()

g = PyGlobe()
g.plot('live','live','locate','show')