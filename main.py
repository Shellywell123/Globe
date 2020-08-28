import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from MPLP import *
import random

################################################################################

class PyGlobe:

    def spherical_to_cartesian(self,theta,phi,radius):
        """
        simple spherical to cartesian coord transform
        """
        x = radius * np.sin(theta) * np.cos(phi)
        y = radius * np.sin(theta) * np.sin(phi)
        z = radius * np.cos(theta)

        return x,y,z

    def degrees_to_radians(self,angle):
        """
        degrees to radians angle converter
        """
        angle = float(angle/180)*np.pi
        return angle

    def cartesian_transformation_radial(self,x,y,z,orbit_radius,orbital_inclination):
        """
        orbiatal position and inclination
         
        """
        orbital_inclination = self.degrees_to_radians(orbital_inclination)

        x = x
        y = y + orbit_radius
        z = z
        return x,y,z


    def cartesian_transformation_obliquity(self,x,y,z,obliquity):
        """
        converts cartesian coords to cartesian coords with a obliquity tilt 
        """
        obliquity = self.degrees_to_radians(-obliquity)
        z =  z*np.cos(obliquity) + x*np.sin(obliquity)
        x = -z*np.sin(obliquity) + x*np.cos(obliquity)
        return x,y,z

    def coordinate_selector(self,longitude,latitude):
        """
        will indicate a point on earth with a point plotted on the globe
        """
        longitude = self.degrees_to_radians(longitude)
        latitude  = self.degrees_to_radians(latitude)

        x,y,z=self.spherical_to_cartesian(longitude,latitude,body_radius)

        ax.plot([x,x+100],[y,y+100],[z,z+100],c='r')

        
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
 
    def spherical_body(self,ax,name,image_file,body_radius,obliquity,orbit_radius,orbital_inclination):
        """
        generates a rendered spherical body
        """

        img = plt.imread(image_file)

        # define a grid matching the map size, subsample along with pixel    
        theta = np.linspace(0, np.pi, img.shape[0])
        phi   = np.linspace(0, 2*np.pi, img.shape[1])

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
        #orbit dist and inclination
        x,y,z = self.cartesian_transformation_radial(x,y,z,orbit_radius,orbital_inclination)

        if orbit_radius != 0:
            
            self.plot_orbit(ax,'grey',orbit_radius,orbital_inclination)

        ax.plot_surface(x.T, y.T, z.T, facecolors=img/255, cstride=1, rstride=1)
        print('Created {}'.format(name))


    def starry_night(self,ax,max_lim,num_of_Stars):
        """
        plots random stars in foreground and background
        """
        
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
        print('Created Stars')

################################################################################

if __name__ == "__main__":
    g = PyGlobe()

    fig = plt.figure('Globe')
    ax = fig.add_subplot(111, projection='3d')

    #set axis lims
    max_lim =  13000
    min_lim = -max_lim
    
    ax.set_xlim3d([min_lim,max_lim])
    ax.set_xlabel('km')
    
    ax.set_ylim3d([min_lim,max_lim])
    ax.set_ylabel('km')
    
    ax.set_zlim3d([min_lim,max_lim])
    ax.set_zlabel('km')

    ######################################################################################
    # Space
    star_distance   = max_lim*5
    number_of_stars = 6000
    g.starry_night(ax,star_distance,number_of_stars)

    #use Equirectangular projections for img files

    ######################################################################################
    # Earth

    name                = 'Earth'
    img                 = 'surfaces/earth.jpg'
    body_radius         = 6378 #km
    radial_position     = 0 #km
    obliquity           = 23.5 #degs
    orbital_inclination = 0
    g.spherical_body(ax,name,img,body_radius,obliquity,radial_position,orbital_inclination)

    ######################################################################################
    # Moon

    name                = 'Moon'
    img                 = 'surfaces/moon.jpg'
    body_radius         = 1737.5 #km
    radial_position     = 12000 #km (should be 384000)
    obliquity           = -6.7 #degs
    orbital_inclination = 5
    g.spherical_body(ax,name,img,body_radius,obliquity,radial_position,orbital_inclination)

    ######################################################################################

    #g.coordinate_selector(0,0)

    MPL_Prefs(fig,ax,'','grid')
    plt.show()
