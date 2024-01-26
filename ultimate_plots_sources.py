import numpy as np
import matplotlib.pyplot as plt
import random 
import seaborn as sns
import pandas as pd
import os

'''
looking at each set of source data, plotting ultimate plot for each
'''
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

elements_list = ["Co_60","Cs_137", "Fe_55"]

for element in elements_list:

    dir_path="MAPS_RR\source_data"
    pathway = os.path.join(dir_path, element, "Towards_sensor")
    list=os.listdir(pathway)
    # gets all items in the Towards_sensor folder

    all_ims = np.zeros((200*len(list),520,520))
    for count, item in enumerate(list):
        # runs over all relevant .raw files and image formats them, adds them into the main element image array
        filename = os.path.join(pathway, item)
        im = format_image(filename)
        all_ims[count*200:(count+1)*200,:,:] = im

    # calculates pedestal and noise, runs 4 sigma cut and re-calculates pedestal and mean
    pedestal = all_ims.mean(axis=0)
    noise = all_ims.std(axis=0)
    shape_im = np.shape(all_ims)
    n_frames=shape_im[0]

    mask = np.where(abs(all_ims) > pedestal+4*noise)

    all_ims[mask] = 0

    pedestal=all_ims.mean(axis=0)
    noise = all_ims.std(axis=0)

    # plotting ultimate plot for some random pixels
    a = (all_ims-pedestal)/noise 

    num_pixels=1
    image_size=(520,520)
    rand_indexes=np.zeros((num_pixels,2))

    for i in range(0,num_pixels): # choose some random pixels on the sensor
        rand_indexes[i,0]=random.randint(0,image_size[0]-1)
        rand_indexes[i,1]=random.randint(0,image_size[1]-1)

        x_coord = int(rand_indexes[i,0])
        y_coord = int(rand_indexes[i,1])

        a_pix=a[:,x_coord,y_coord]
        fig, ax = plt.subplots(1,1)
        ax.hist(a_pix, bins=70)
        ax.set_title(f"Ultimate Plot for {element}, at Pixel [{x_coord}, {y_coord}]")
        plt.savefig(f"ultimate_plot_{element}.png")
        



            










