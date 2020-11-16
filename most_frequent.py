#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 19:35:22 2020

@author: simon
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import cv2
import os


'''
Carga y tratamiento de la imagen
'''
def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename),cv2.IMREAD_UNCHANGED)
        if img is not None:
            images.append(img)
    return images

def resize_image(img,width,height):
    dim = (width, height)
    
    interp=cv2.INTER_AREA
    if(dim > img.shape):
        interp=cv2.INTER_LINEAR
        #interp=cv2.INTER_CUBIC
    
    resized = cv2.resize(img, dim, interpolation = interp)
    
    return resized

def resize_image_by_percent(img,scale_percent):
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    
    interp=cv2.INTER_AREA
    if(scale_percent>100):
        interp=cv2.INTER_LINEAR
        #interp=cv2.INTER_CUBIC
    
    resized = cv2.resize(img, dim, interpolation = interp)
    return resized

def print_image(img):
    cv2.imshow("Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def print_image_matplotlib(img):
    plt.figure(figsize=(16,16))
    plt.imshow(img[:,:,::-1])
    plt.axis('off')
    plt.show()




'''
Cálculo del color más común en la foto
'''
# Utilizando la media
def mostCommon_Average(img):
    media = np.average(img, axis=(0,1))
    return np.array([media])

# Contando el número de píxeles 
def mostCommon_PixelCount(img,n=5,redu=16):
    # Reducimos el número de colores a contar.
    img_tmp = img.copy()
    img_tmp = img_tmp/redu
    img_tmp = img_tmp.astype('uint8')
    
    unique, counts = np.unique(img_tmp.reshape(-1, 3), axis=0, return_counts=True)
    indexes=np.arange(len(counts))
    zipped_list=zip(counts,indexes)
    
    indexes_sort = [element for _, element in sorted(zipped_list,reverse=True)]

    return unique[indexes_sort[:n]]*redu

def mostCommon_AveragePixelCount(img,n=5,redu=16):
    colors=mostCommon_PixelCount(img,n,redu)
    media = np.average(colors,axis=0)
    return np.array([media])

# Utilizando clustering
def mostCommon_KMeans(img):
    kmeans=KMeans(n_clusters=5,random_state=123456789)
    clusters = kmeans.fit(img.reshape(-1, 3))
    unique, counts = np.unique(clusters.labels_, axis=0, return_counts=True)
    zipped_list=zip(counts,unique)
    labels_sort = [element for _, element in sorted(zipped_list,reverse=True)]

    return kmeans.cluster_centers_[labels_sort]

# Dibujar los colores obtenidos (la variable color está en BGR)
def plotColors(colors,name=""):
    print("Colores obtenidos de " + name)
    print(colors)
    x=np.array([0,1])
    y=np.array([5,5])
    fig, ax = plt.subplots()
    
    for color in colors:
        # Usamos color[::-1] porque OpenCV trabaja con BGR en vez de RGB
        ax.plot(x,y,linewidth=37,color=color[::-1]/255)
        y=y-1
        
    ax.xaxis.set_visible(False)
    ax.set_yticklabels([])
    plt.ylabel('-> More Common ->')
    plt.title(name)
    plt.show()

# Comparar la imagen con los colores más comunes
def compare_img_commonColor(img, colors):
    ncolors=len(colors)
    height=img.shape[0]
    width=img.shape[1]
    img_color = np.empty([height,width,3],dtype='uint8')
    for i in range(ncolors):
        img_color[:,i*int(width/ncolors):i*width+int(width/ncolors)] = colors[i][::-1]
    
    fig, ax = plt.subplots(1, 2, figsize=(5,5))
    ax[0].imshow(img[:,:,::-1])
    ax[1].imshow(img_color)
    
    ax[0].axis('off')
    ax[1].yaxis.set_visible(False)
    ax[1].set_xticklabels([])
    ax[1].set_xlabel('<- More Common <-')
    
    fig.tight_layout()
    plt.show()



'''
Dividir la imagen y buscar la más similar
'''
def find_nearest(colors, color):
    dists = np.linalg.norm(colors-color,axis=1)
    idx = dists.argmin()
    
    return colors[idx]

def find_idx_nearest(colors, color):
    dists = np.linalg.norm(colors-color,axis=1)
    idx = dists.argmin()
    
    return idx

# Función principal
def TroyaMosaic(img,mosaic_imgs,n_photos,mostCommon):
    height = img.shape[0]
    width = img.shape[1]
    
    size_mosaic = int(height/n_photos)
    
    mosaic_colors=np.empty([0,3],int)
    
    for i in range(len(mosaic_imgs)):
        mosaic_imgs[i] = resize_image(mosaic_imgs[i],size_mosaic,size_mosaic)
        mosaic_colors=np.vstack((mosaic_colors,mostCommon(mosaic_imgs[i],n=1)))
    
    
    for i in np.arange(0,height,size_mosaic):
        for j in np.arange(0,width,size_mosaic):
            cuadradito = img[i:i+size_mosaic,j:j+size_mosaic]
            common_color = mostCommon(cuadradito,redu=1,n=1)
            idx = find_idx_nearest(mosaic_colors,common_color)
            img[i:i+size_mosaic,j:j+size_mosaic] = mosaic_imgs[idx]
    
    return img
    


def main():
    main_img = cv2.imread('./images/troyita.png', cv2.IMREAD_UNCHANGED)
    main_img = resize_image(main_img,2500,2500)
    
    mosaic_imgs = load_images_from_folder('./images/mosaic/')
    
    result = TroyaMosaic(main_img,mosaic_imgs,250,mostCommon_PixelCount)
    
    print("Done!\n")
    
    #print_image(result)
    print_image_matplotlib(result)
    
    #cv2.imwrite('resultado.png',result,[cv2.IMWRITE_PNG_COMPRESSION, 9])
    
    '''
    resized = resize_image(main_img,500,500)
    color_average = mostCommon_Average(resized)
    colors_pixel = mostCommon_PixelCount(resized,redu=32)
    colors_kmeans = mostCommon_KMeans(resized)
    
    plotColors(color_average, name="Average")
    plotColors(colors_pixel, name="Pixel Count")
    plotColors(colors_kmeans, name="KMeans")
    '''
    

if __name__ == "__main__":
    main()
