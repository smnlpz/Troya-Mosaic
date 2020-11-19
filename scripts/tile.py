#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 18:11:15 2020

@author: simon
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from scripts.large_image import LargeImage

class Tile(LargeImage):
    __colors = np.empty([0,3],dtype='uint8')
    
    def __init__(self, img):
        super().__init__(img)
    
    def getColor(self):
        return self.__colors
    
    
    '''
    Operaciones
    '''
    def getDiff_by_color(self,tile):
        # La raíz cuadrada es muy costosa computacionalmente,
        # y no es necesaria para nuestro resultado
        # dist = np.linalg.norm(self.__colors[0]-tile.__colors[0])
        dist = (self.__colors[0][0]-tile.__colors[0][0])*(self.__colors[0][0]-tile.__colors[0][0])+ \
        (self.__colors[0][1]-tile.__colors[0][1])*(self.__colors[0][1]-tile.__colors[0][1])+ \
        (self.__colors[0][2]-tile.__colors[0][2])*(self.__colors[0][2]-tile.__colors[0][2])
        
        return dist
    
    def getDiff_by_pixel(self,tile):
        dist = 0
        for i in range(self._img.shape[0]):
            for j in range(self._img.shape[1]):
                dist += (int(self._img[i,j,0])-int(tile._img[i,j,0]))*(int(self._img[i,j,0])-int(tile._img[i,j,0]))+ \
                (int(self._img[i,j,1])-int(tile._img[i,j,1]))*(int(self._img[i,j,1])-int(tile._img[i,j,1]))+ \
                (int(self._img[i,j,2])-int(tile._img[i,j,2]))*(int(self._img[i,j,2])-int(tile._img[i,j,2]))
        
        return dist
    
    
    '''
    Cálculo del color más común en la foto
    '''
    # Utilizando la media
    def mostCommon_Average(self,n=1,redu=1):
        media = np.average(self._img, axis=(0,1))
        self.__colors = np.array([media])
        
        return self.__colors
    
    # Contando el número de píxeles 
    def mostCommon_PixelCount(self,n=5,redu=16):
        # Reducimos el número de colores a contar.
        img_tmp = self._img.copy()
        img_tmp = img_tmp/redu
        img_tmp = img_tmp.astype('uint8')
        
        unique, counts = np.unique(img_tmp.reshape(-1, 3), axis=0, return_counts=True)
        indexes=np.arange(len(counts))
        zipped_list=zip(counts,indexes)
        
        indexes_sort = [element for _, element in sorted(zipped_list,reverse=True)]
    
        self.__colors = unique[indexes_sort[:n]]*redu
        
        return self.__colors
    
    def mostCommon_AveragePixelCount(self,n=5,redu=16):
        colors = self.mostCommon_PixelCount(n,redu)
        media = np.average(colors,axis=0)
        self.__colors = np.array([media])
        
        return self.__colors
    
    # Utilizando clustering
    def mostCommon_KMeans(self,n=1,redu=1):
        kmeans=KMeans(n_clusters=5,random_state=123456789)
        clusters = kmeans.fit(self._img.reshape(-1, 3))
        unique, counts = np.unique(clusters.labels_, axis=0, return_counts=True)
        zipped_list=zip(counts,unique)
        labels_sort = [element for _, element in sorted(zipped_list,reverse=True)]
    
        self.__colors = kmeans.cluster_centers_[labels_sort[0:n]]
        
        return self.__colors
    
    '''
    Muestras por pantalla
    '''    
    # Dibujar los colores obtenidos (la variable color está en BGR)
    def plotColors(self,name=""):
        ncolors=len(self.__colors)
        height=self._img.shape[0]
        width=self._img.shape[1]
        img_color = np.empty([height,width,3],dtype='uint8')
        for i in range(ncolors):
            img_color[:,i*int(width/ncolors):i*width+int(width/ncolors)] = self.__colors[i][::-1]
        
        fig, ax = plt.subplots()
        ax.imshow(img_color)
        
        ax.yaxis.set_visible(False)
        ax.set_xticklabels([])
        ax.set_xlabel('<- More Common <-')
        
        plt.show()

    def compare_img_commonColor(self):
        ncolors=len(self.__colors)
        height=self._img.shape[0]
        width=self._img.shape[1]
        img_color = np.empty([height,width,3],dtype='uint8')
        for i in range(ncolors):
            img_color[:,i*int(width/ncolors):i*width+int(width/ncolors)] = self.__colors[i][::-1]
        
        fig, ax = plt.subplots(1, 2, figsize=(5,5))
        ax[0].imshow(self._img[:,:,::-1])
        ax[1].imshow(img_color)
        
        ax[0].axis('off')
        ax[1].yaxis.set_visible(False)
        ax[1].set_xticklabels([])
        ax[1].set_xlabel('<- More Common <-')
        
        fig.tight_layout()
        plt.show()
        
