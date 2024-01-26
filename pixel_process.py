import numpy as np
import matplotlib.pyplot as plt
import random 
import seaborn as sns
import pandas as pd
'''
Importing, formatting and cleaning .raw data from MAPS. Removes 'dodgy' first few frames of data.
'''


# import data from file, with correct data type
filename= "MAPS_RR\PTC_data_2\data_1.3V_data.raw"



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


frame_1=im[:,100,100] # slicing off just the first frame to plot

# plt.imshow(frame_1)
# plt.show()

# faulty pixel if frame_1[i]> mean=3*sig

# # flattening frame 1 to plot histogram
# frame_1_flat=np.ravel(frame_1)
# flat=np.ravel(im)
# pedestal=im.mean(axis=0)
# flat=flat
# fig, ax=plt.subplots(1,1)
# ax.hist(flat, bins= 100)
# ax.set_title("Pedestal-corrected signal distribution for one pixel over all frames")
# plt.savefig("MAPS_RR\PTC_data\signal_dist_corrected.png")
# plt.show()

std_all=im.std(axis=0)
pedestal=im.mean(axis=0) # the pedestal
# print(np.shape(pedestal))
# print(np.shape(im))
# for a given pixel is the value >3sig from mean (for all image)? if yes then broken


# plt.imshow(pedestal, cmap='plasma')

# plt.clim(pedestal.min()+200, pedestal.max()-200)
# plt.title("Mean of Pixels (All Frames)")
# plt.colorbar()
# plt.show()



# pedestal correction for image

frame_no=100
filename_2=R"MAPS_RR\PTC_data_4\data_3.6_data.raw"
raw_event=format_image(filename_2, num_drop=1)
raw_event=raw_event[frame_no,:,:]
corrected_event=raw_event

plt.imshow(corrected_event, cmap='plasma')
plt.title("Raw Event Plot")
plt.colorbar()
#plt.savefig(R"MAPS_RR\PTC_data\raw_plot.png")
plt.show()