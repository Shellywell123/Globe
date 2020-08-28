import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from MPLP import *
import random

################################################################################

class PyGlobe:

    def spherical_to_cartesian(self,theta,phi,R):
        """
        """
        x = R * np.sin(theta) * np.cos(phi)
        y = R * np.sin(theta) * np.sin(phi)
        z = R* np.cos(theta)

        return x,y,z

    def cartesian_transformation_tilt(self,x,y,z,tilt,Rpos):
        """
        """
        tilt = float(-tilt/180)*np.pi
        z = z*np.cos(tilt) + x*np.sin(tilt)
        x = Rpos -z*np.sin(tilt) + x*np.cos(tilt)
        return x,y,z

    def coordinate_selector(self):
        """
        """
        return None
 
    def spherical_body(self,ax,name,image_file,R,tilt,Rpos):
        """
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
        x,y,z = self.spherical_to_cartesian(theta,phi,R)
        x,y,z = self.cartesian_transformation_tilt(x,y,z,tilt,Rpos)

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

    # create 3d Axes
    fig = plt.figure()
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

    g.starry_night(ax,max_lim*5,6000)

    #use Equirectangular projections for img files
    earth_img = 'surfaces/earth.jpg'
    earth_radius          = 6378 #km
    earth_radial_position = 0 #km
    earth_tilt            = 23.5 #degs
    g.spherical_body(ax,'Earth',earth_img,earth_radius,earth_tilt,earth_radial_position)

    moon_img = 'surfaces/moon.jpg'
    moon_radius          = 1737.5 #km
    moon_radial_position = 12000 #km (should be 384000)
    moon_tilt            = 6.7 #degs
    g.spherical_body(ax,'Moon',moon_img,moon_radius,moon_tilt,moon_radial_position)

    MPL_Prefs(fig,ax,'','grid')
    plt.show()