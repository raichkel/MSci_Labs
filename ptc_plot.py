import numpy as np
import matplotlib.pyplot as plt
import random 
import seaborn as sns
import pandas as pd
import os

# import data from file, with correct data type
file= "MAPS_RR\PTC_data_4\data_1.7_data.raw"



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



# n_indexes=1
# image_size=(520,520)
# rand_indexes=np.zeros((n_indexes,2))

# for i in range(0,n_indexes):
#     rand_indexes[i,0]=random.randint(0,image_size[0]-1)
#     rand_indexes[i,1]=random.randint(0,image_size[1]-1)
pedestal=dark.mean(axis=0)


def get_snr(im, rand_indexes, n_pixels):
    '''
    takes image and returns the signal and noise for some pre-selected random points
    '''
    shape=np.shape(im)
    n_frames=shape[0]
    # empty array that will store signal and noise data for each pixel
    pixel_points=np.zeros((n_pixels, 2))
    
    signal=np.zeros((n_frames, 520,520))

    std_all=im.std(axis=0) 
    for l in range(0,n_frames):
            
            signal[l,:,:]=im[l,:,:]

    sig_avg=signal.mean(axis=0)
    
    
    for j,i in enumerate(rand_indexes):
        # looping over each randomly selected coordinate and finding signal and noise
        
        
        x=int(i[0])
        y=int(i[1])
        # pick coordinate
        # for that pixel, pedestal correct all frames
        
            
        
        # take mean of that pixel (corrected) over all frames
        sig_point=sig_avg[x,y]
        if(sig_point<0):
            break
        else:
            # find sd of that pixel
            noise_point=std_all[x,y]
            # output tuple of signal and noise
            
            pixel_points[j,0]=sig_point
            pixel_points[j,1]=noise_point
        
    return pixel_points

def ptc_curve(num_pixels=4):

    '''
    reads in num_points number of data files, 
    '''

    image_size=(520,520)
    rand_indexes=np.zeros((num_pixels,2))
    
    for i in range(0,num_pixels):
        rand_indexes[i,0]=random.randint(0,200)
        rand_indexes[i,1]=random.randint(100,200)
    
    
    dir_path="MAPS_RR\PTC_data_4"
    list=os.listdir(dir_path)
    num_points=len(list)
    # create array to store signa and noise values for num_pixels no. of pixels, for every data set (num_points)
    arr=np.zeros((num_points,num_pixels, 2))
    for count,item in enumerate(list):

        filename=os.path.join(dir_path, item)
        im=format_image(filename, num_drop=5)
        pixel_points=get_snr(im, rand_indexes,num_pixels)
        
        arr[count,:,:]=pixel_points
        #print(arr[i,:,:])
    # arr[a,b,c]: a indexes the dataset that the values will be from, b indexes the pixel that the data will be from,
    # c indexes the component of the data we are looking at (signal=0, noise=1)
    #print(arr[:,:,0])
    # pixel_points[:,0] is sig, pixel_points[:,1] is noise

    fig, ax = plt.subplots(2,2, sharex=True, sharey=True)
    # print(arr[:,0,0])
    # print(arr[:,0,1])
    pix_no=0
    
    for i in range(0,2):
        for j in range(0,2):
            for a in (arr[:,pix_no,1])**2:
                if a> 250:
                    a=250
                
            x_coord = rand_indexes[pix_no,0]
            y_coord = rand_indexes[pix_no, 1]
            ax[i,j].scatter(arr[:,pix_no,0], (arr[:,pix_no,1])**2, color="purple")
            ax[i,j].set_ylim(0,250)
            ax[i,j].set_xlabel("Average Signal")
            ax[i,j].set_ylabel("Noise^2")
            ax[i,j].set_title(f"Pixel:{x_coord}, {y_coord} ")
            c_arr = np.polyfit(arr[:30,pix_no,0],(arr[:30,pix_no,1])**2, 1)
            ax[i,j].plot(arr[:30,pix_no,0], c_arr[0]*arr[:30,pix_no,0]+c_arr[1], color="magenta", linestyle="dashed")
            print(f"plot {x_coord}, {y_coord}: m = {c_arr[0]}, c = {c_arr[1]}")
            pix_no+=1
    fig.suptitle("PTC")
    plt.tight_layout()
    plt.savefig("MAPS_RR\ptc_3.png")
    plt.show()

ptc_curve(4)




