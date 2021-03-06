#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 18:58:59 2020

@author: simon
"""

import numpy as np
import matplotlib.pyplot as plt
import cv2

class LargeImage:
    def __init__(self, img=np.empty([0,0,3])):
        self._img = img
        self.shape = img.shape
        
        if self.shape[2] == 4:
            self.bgra2bgr()
        
    def __getitem__(self, key):
        return self._img[key]
    
    def __setitem__(self, key, item):
        self._img[key]=item
    
    def copy(self):
        return LargeImage(self._img.copy())
    
    # Devuelve la matrix de píxeles de la imagen
    def getData(self):
        return self._img
    
    # Comprueba si la imagen está vacía
    def isEmpty(self):
        if self.shape[0:2] == (0,0):
            return True
        else:
            return False
    
    # Redimensionar imagen dados un ancho y un alto
    def resize_image(self, width, height):
        dim = (width, height)
        
        # La interpolación es diferente en función de si
        # el nuevo tamaño es mayor o menor
        interp=cv2.INTER_AREA
        if(dim > self._img.shape):
            interp=cv2.INTER_LINEAR
        
        self._img = cv2.resize(self._img, dim, interpolation = interp)
        self.shape = self._img.shape
    
    # Redimensionar imagen dado un porcentaje de escalado
    def resize_image_by_percent(self, scale_percent):
        height = int(self._img.shape[0] * scale_percent / 100)
        width = int(self._img.shape[1] * scale_percent / 100)
        
        dim = (width, height)
        
        # La interpolación es diferente en función de si
        # el nuevo tamaño es mayor o menor
        interp=cv2.INTER_AREA
        if(scale_percent>100):
            interp=cv2.INTER_LINEAR
        
        self._img = cv2.resize(self._img, dim, interpolation = interp)
        self.shape = self._img.shape
    
    # Convierte la imagen de formato BGRA (BGR con transparencia) a BGR
    def bgra2bgr(self):
        blue = self._img[:,:,0]
        green = self._img[:,:,1]
        red = self._img[:,:,2]
        alpha = self._img[:,:,3]
        
        self._img[:,:,0] = (1-alpha)*blue + alpha*blue
        self._img[:,:,1] = (1-alpha)*green + alpha*green
        self._img[:,:,2] = (1-alpha)*red + alpha*red
        
        self._img = self._img[:,:,:3]
    
    # Rotar la imagen a la izda o a la dcha
    def rotate_image(self, orient):
        if orient ==  'right':
            self._img = cv2.rotate(self._img,cv2.ROTATE_90_CLOCKWISE)
        elif orient == 'left':
            self._img = cv2.rotate(self._img,cv2.ROTATE_90_COUNTERCLOCKWISE)
        self.shape = self._img.shape
            
 
    # Muestra la imagen por pantalla
    def plot(self, mode = 'cv2'):
        if mode == 'cv2':
            cv2.imshow("Image", self._img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        elif mode == 'plt':
            plt.figure(figsize=(16,16))
            plt.imshow(self._img[:,:,::-1]) # CV2 almacena las imágenes en BGR, no en RGB
            plt.axis('off')
            plt.show()

    def __str__(self):
        return str(self._img)