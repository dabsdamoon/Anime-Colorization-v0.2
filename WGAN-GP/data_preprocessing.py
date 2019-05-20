import numpy as np
import matplotlib.pyplot as plt

from skimage.color import rgb2gray, rgb2lab, lab2rgb


##### Defining global parameters

size_row = 128
size_col = 128
latent_dim = 100


##### Function for creating LAB feature and label image (L for feature, and AB for label)

def create_feature_label_image(image_resized):
    
    # create 3 dimensional gray image with rgb2gray * 3
    image_gray = rgb2gray(image_resized).reshape(size_row, size_col, 1) # this will be the validation dataset
    image_gray3 = np.concatenate([image_gray]*3, axis = 2)
    image_lab3 = rgb2lab(image_gray3)
    image_feature = image_lab3[:,:,0]/128 # scaling from -1 to 1

    # create label first with rgb2lab image
    image_lab = rgb2lab(image_resized)
    image_label = image_lab[:,:,1:]/128 # scaling from -1 to 1
    
    return image_feature, image_label # return feature would be 1st column of lab image generated by gray3 image


##### Function for visualization

def sample_images(gen_imgs):

    if gen_imgs.shape[3] == 1:
        chosen_cmap="gray"
    else:
        chosen_cmap=None

    r, c = 5,5
    fig, axs = plt.subplots(r, c, figsize = (15, 15))
    cnt = 0
    
    for i in range(r):
        for j in range(c):
            if chosen_cmap=="gray":
                img_to_show = gen_imgs[cnt,:,:,0]
            else:
                img_to_show = lab2rgb(gen_imgs[cnt,:,:,:])
                
            img_to_show = np.where(img_to_show >= 0, img_to_show, 1e-4)
            axs[i,j].imshow(img_to_show, cmap=chosen_cmap)
            axs[i,j].axis('off')
            cnt += 1
            
    plt.show()
    plt.close()


##### Function for generating different noises

def custom_noise(latent_dim = latent_dim, sequence_num = 5, interval = 1, interval_order = [-2,-1,0,1,2]):
    
    seq_length = int(latent_dim / sequence_num)

    noise_vec = []

    for s in range(sequence_num):

        for i in interval_order: # total length = sequence_num * len(interval_order)

            noise_original = np.zeros((1, latent_dim))
            noise_original[:, (s)*seq_length:(s+1)*seq_length] = noise_original[:, (s)*seq_length:(s+1)*seq_length] + interval*i

            noise_vec.append(noise_original)

    return np.concatenate(noise_vec, axis = 0)


##### Function for displaying image on notebook

def show_image(input_mat, figure_size = (4,4)):
    plt.figure(figsize = figure_size)
    plt.axis("off")
    plt.imshow(input_mat)
    plt.show()