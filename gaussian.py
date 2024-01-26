import numpy as np
import matplotlib.pyplot as plt
import random 
import seaborn as sns
import pandas as pd
import os

# import data from file, with correct data type
file= "MAPS_RR\PTC_data\data_01_data.raw"



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

dark=format_image(file, num_drop=1)
pedestal = dark.mean(axis=0)

dir_path="MAPS_RR\PTC_data_2"
list=os.listdir(dir_path)
num_points=len(list)



list=list[5:]
fig, ax=plt.subplots(1,1)
for count,item in enumerate(list):

    filename=os.path.join(dir_path, item)
    im=format_image(filename, num_drop=1)

    pix_flat=np.ravel(im)
    ax.hist(pix_flat, bins= 100)

ax.set_title("Histogram of pixels across different light intensities")
plt.savefig("MAPS_RR\hist.png")
plt.show()
   