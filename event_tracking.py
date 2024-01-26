import numpy as np
import matplotlib.pyplot as plt
import random 
import seaborn as sns
import pandas as pd



# import data from file, with correct data type
filename= "MAPS_RR\PTC_data\data_01_data.raw"



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
shape=np.shape(im)

pedestal=im.mean(axis=0)
nFrames=shape[0]

random_x_coord= np.random.randint(521)
random_y_coord= np.random.randint(521)
pixel_response= np.zeros(nFrames)
pixel_response_corrected=np.zeros(nFrames)
frame_number= np.arange(0,200,1)

# finding the response for a random pixel
for i in range (nFrames):
    pixel_response[i]= im[i,random_x_coord,random_y_coord]
    # correcting for the pedestal for the pixel
    pixel_response_corrected[i]= im[i,random_x_coord,random_y_coord]-pedestal[random_x_coord,random_y_coord]


fig, ax = plt.subplots(2,1, sharex=True)
ax[0].plot(pixel_response)
ax[0].set_title('Raw Pixel Response Over Every Frame For One Pixel')
ax[1].plot(pixel_response_corrected)
ax[1].set_title('Pedestal Corrected Pixel Response Over Every Frame For One Pixel')
plt.show()