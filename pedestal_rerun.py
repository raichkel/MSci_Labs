import numpy as np
import matplotlib.pyplot as plt
import random 
import seaborn as sns
import pandas as pd



# import data from file, with correct data type
filename= "MAPS_RR\Fe_55\Towards_sensor\data_towards_3_data.raw"



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

im=format_image(filename, num_drop=1)



pedestal = im.mean(axis=0)
noise = im.std(axis=0)
shape_im = np.shape(im)
n_frames=shape_im[0]

mask = np.where(abs(im) > pedestal+4*noise)

im[mask] = 0

pedestal_new=im.mean(axis=0)

plt.imshow(pedestal_new, cmap = 'inferno')
plt.colorbar()
plt.title("New Pedestal Calculated from $\pm4\sigma$ Cut")
plt.savefig("pedestal_new.png")
