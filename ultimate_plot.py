import numpy as np
import matplotlib.pyplot as plt
import random 
import seaborn as sns
import pandas as pd
import os
from scipy.stats import norm

# import data from file, with correct data type
file= "MAPS_RR\PTC_data_3\data_1.6_data.raw"



def format_image(filename, num_drop=5, image_size=(520,520)):

    '''
    Import, clean and format pixel data from .raw file.

    Inputs:
    - filename: string, relative path to .raw file containing data
    - num_drop: int, no. of 'dodgy' frames to drop before returning data
    - image_size: tuple of ints, size of frame in pixels

    Outputs:
    - image: NumPy array, 3-D array of image_size sized frames
    '''
    image=np.fromfile(filename,dtype='uint16') 

    x=image_size[0]
    y=image_size[1]

    pixels_per_frame=x*y+2 # add 2 extra pixels that are saved in with metadata

    num_frames=int(image.size/pixels_per_frame) # total no. of frames in dataset

    image=image.reshape([num_frames,pixels_per_frame]) # reshape to list of frames

    image=image[num_drop:,2:] # slices off first 5 frames and first 2 pixels

    image=image.reshape([num_frames-num_drop,x,y]) # reshapes to 3-D array of 2-D frames

    return image

dark=format_image(file, num_drop=1) # importing data for pedestal
pedestal=dark.mean(axis=0)

filename="MAPS_RR\Fe_55\Towards_sensor\data_towards_3_data.raw"

im = format_image(filename) # importing Fe-55 data
noise=im.std(axis=0) 

a=(im-pedestal)/noise # calculating a

num_pixels=4
image_size=(520,520)
rand_indexes=np.zeros((num_pixels,2))

for i in range(0,num_pixels): # choose some random pixels on the sensor
    rand_indexes[i,0]=random.randint(0,image_size[0]-1)
    rand_indexes[i,1]=random.randint(0,image_size[1]-1)

fig,ax = plt.subplots(2,2)


for j,i in enumerate(rand_indexes): 
    # looping over each randomly selected coordinate
    x_coord=int(i[0])
    y_coord=int(i[1])
    # pick coordinate
   
    a_pix=a[:,x_coord,y_coord]
    
    if j<2:
        row=0
        y,x,_ = ax[row,j].hist(a_pix, bins=50)
        mu, std = norm.fit(a_pix)
        ymax=y.max()
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = norm.pdf(x, mu, std)
        ax[row,j].set_title(f"Pixel: [{x_coord},{y_coord}]")
        ax[row,j].plot(x,ymax*p)
    elif j>=2 and j<4:
        row=1
        y,x,_ = ax[row, j-2].hist(a_pix, bins=50)
        mu, std = norm.fit(a_pix)
        ymax=y.max()
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = norm.pdf(x, mu, std)
        ax[row,j-2].set_title(f"Pixel: [{x_coord},{y_coord}]")
        ax[row,j-2].plot(x,ymax*p)


fig.suptitle("Ultimate Plot")
plt.tight_layout()
plt.savefig("ultimate_fe.png")
plt.show()


