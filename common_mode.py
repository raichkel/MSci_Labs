from doctest import DocFileCase
import numpy as np
import matplotlib.pyplot as plt
import random 
import seaborn as sns
import pandas as pd
'''
Finding common mode by looking at sns.pairplot correlations for pixels surrounding some randomly chosen pixels
'''


# import data from file, with correct data type
filename= "MAPS_RR\Dark_data\Dark_data_200_data.raw"

# test
def format_image(filename, num_drop=5, image_size=(520,520)):

    '''
    Import, clean and format pixel data from .raw file.

    Inputs:
    - filename: string, ralative path to .raw file containing data
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

# set no. of random pixels to select
n_indexes=1
image_size=(520,520)

# selecting n_indexes random pixels from the im (image) array
rand_indexes=np.zeros((n_indexes,2))

for i in range(0,n_indexes):
    rand_indexes[i,0]=random.randint(0,image_size[0]-1)
    rand_indexes[i,1]=random.randint(0,image_size[1]-1)

rand_indexes=rand_indexes.astype(int)
ind=0
for i in rand_indexes:
    # for each randomly selected index, choose the pixels surrounding it in a 3x3 square
    n_frames=im.shape[0]
    
    pix_arr=np.zeros((n_frames,9))
    # pick the pixel at i[0], i[1]
    pix=im[:,i[0],i[1]]
    
    pix_arr[:,4]=pix
    # pick the 8 pixels all around it and save them as a separate array
    indexer=0
    for n in range (-1, 2):
        for m in range(-1, 2):
            pix=im[:,i[0]+n, i[1]+m]
            pix_arr[:,indexer]=pix
            indexer+=1
    # save the array as a dataframe and do a correlation plot on all the pixels
    df=pd.DataFrame(pix_arr)
    print(df)
    sns.pairplot(df)
    plt.savefig(f"MAPS_RR\Dark_data\pairplot_{ind}.png")
    ind+=1


            