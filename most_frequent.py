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



'''
Carga y tratamiento de la imagen
'''
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


'''
Cálculo del color más común en la foto
'''
# Utilizando la media
def mostCommon_Average(img):
    media = np.average(img, axis=(0,1))
    return np.array([media])

# Contando el número de píxeles 
def mostCommon_PixelCount(img,n=5):
    unique, counts = np.unique(img.reshape(-1, 3), axis=0, return_counts=True)
    indexes=np.arange(len(counts))
    zipped_list=zip(counts,indexes)
    
    indexes_sort = [element for _, element in sorted(zipped_list,reverse=True)]

    return unique[indexes_sort[:n]]

# Utilizando clustering
def mostCommon_KMeans(img):
    kmeans=KMeans(n_clusters=5,random_state=123456789)
    clusters = kmeans.fit(img.reshape(-1, 3))
    unique, counts = np.unique(clusters.labels_, axis=0, return_counts=True)
    zipped_list=zip(counts,unique)
    labels_sort = [element for _, element in sorted(zipped_list,reverse=True)]

    return kmeans.cluster_centers_[labels_sort]

# Dibujar los colores obtenidos
def plotColors(colors,name=""):
    print("Colores obtenidos de " + name)
    print(colors)
    x=np.array([0,1])
    y=np.array([5,5])
    fig, ax = plt.subplots()
    
    for color in colors:
        ax.plot(x,y,linewidth=37,color=color/255)
        y=y-1
        
    ax.xaxis.set_visible(False)
    ax.set_yticklabels([])
    plt.ylabel('-> More Common ->')
    plt.title(name)
    plt.show()



def main():
    img = cv2.imread('./images/troyita.png', cv2.IMREAD_UNCHANGED)
    #resized = resize_image_by_percent(img,scale_percent=10)
    resized = resize_image(img,100,100)
    
    color_average = mostCommon_Average(resized)
    colors_pixel = mostCommon_PixelCount(resized)
    colors_kmeans = mostCommon_KMeans(resized)
    
    plotColors(color_average, name="Average")
    plotColors(colors_pixel, name="Pixel Count")
    plotColors(colors_kmeans, name="KMeans")
    
    

if __name__ == "__main__":
    main()
