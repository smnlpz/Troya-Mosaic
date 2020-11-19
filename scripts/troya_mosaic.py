#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 11:36:19 2020

@author: simon
"""

import numpy as np
import cv2
import os

from scripts.large_image import LargeImage
from scripts.tile import Tile

class TroyaMosaic:
    __tiles = []
    
    def __init__(self,img_name,directory_name=None):
        print('Cargando imagen ' + img_name + ' ...\n')
        self.__main_img = LargeImage(cv2.imread(img_name, cv2.IMREAD_UNCHANGED))
        self.__result = self.__main_img.copy()
        self.__result_overlay = self.__main_img.copy()
        
        if directory_name is not None:
            print('Cargando directorio ' + directory_name + '...\n')
            for filename in os.listdir(directory_name):
                self.addTile(os.path.join(directory_name,filename))
    
    def getMainImg(self):
        return self.__main_img
    
    def getTiles(self):
        return self.__tiles
    
    def getResult(self):
        return self.__result
    
    def addTile(self,tile_name):
        img = cv2.imread(tile_name,cv2.IMREAD_UNCHANGED)
        if img is not None:
            self.__tiles.append(Tile(img))
            
    def resize_main(self,width,height):
        self.__main_img.resize_image(width,height)
    
    
    def find_nearest(tiles, cuad, diffType):
        dists = np.array([diffType(tile,cuad) for tile in tiles])
        idx = dists.argmin()
        
        return idx, dists[idx]
    
    def generate_by_color(self,n_photos,mostCommon,redu=1):
        self.__result = self.__main_img.copy()
        mosaic_imgs = self.__tiles.copy()
        
        height = self.__result.shape[0]
        width = self.__result.shape[1]
        
        size_mosaic = int(height/n_photos)
        
        for i in range(len(mosaic_imgs)):
            mosaic_imgs[i].resize_image(size_mosaic,size_mosaic)
            mostCommon(mosaic_imgs[i],redu=redu)
        
        print('Generando resultado...\n')
        
        for i in np.arange(0,height,size_mosaic):
            for j in np.arange(0,width,size_mosaic):
                cuadradito = Tile(self.__result[i:i+size_mosaic,j:j+size_mosaic])
                mostCommon(cuadradito,redu=redu,n=1)
                idx, _ = TroyaMosaic.find_nearest(mosaic_imgs,cuadradito,Tile.getDiff_by_color)
                self.__result[i:i+size_mosaic,j:j+size_mosaic] = mosaic_imgs[idx].getData()
                
        print('Done!\n')
        
    def generate_by_pixel(self,n_photos):
        self.__result = self.__main_img.copy()
        mosaic_imgs = self.__tiles.copy()
        
        height = self.__result.shape[0]
        width = self.__result.shape[1]
        
        size_mosaic = int(height/n_photos)
        
        for i in range(len(mosaic_imgs)):
            mosaic_imgs[i].resize_image(size_mosaic,size_mosaic)
        
        print('Generando resultado...\n')
        
        for i in np.arange(0,height,size_mosaic):
            for j in np.arange(0,width,size_mosaic):
                cuadradito = Tile(self.__result[i:i+size_mosaic,j:j+size_mosaic])
                idx, _ = TroyaMosaic.find_nearest(mosaic_imgs,cuadradito,Tile.getDiff_by_pixel)
                self.__result[i:i+size_mosaic,j:j+size_mosaic] = mosaic_imgs[idx].getData()
                if ((i*height/size_mosaic)/size_mosaic+j/size_mosaic)%((n_photos*n_photos)/10) == 0:
                    print('Fotos añadidas: ' +str((i*height/size_mosaic)/size_mosaic+j/size_mosaic))
                
        print('Done!\n')
        
    
    def maskOverlay(self,alpha):
        self.__result_overlay = LargeImage(cv2.addWeighted(self.__result.getData(), 1-alpha, self.__main_img.getData(), alpha, 0))
    
    def plot(self,mode='cv2',img='result'):
        if img == 'main':
            self.__main_img.plot(mode=mode)
        elif img == 'result':
            self.__result.plot(mode=mode)
        elif img == 'overlay':
            self.__result_overlay.plot(mode=mode)
            
        
    def saveResult(self,name,compression='Yes',overlay='No'):
        print('Guardando imagen '+ name + ' ...\n')
        
        to_save = self.__result.getData()
        
        if overlay == 'Yes':
            to_save = self.__result_overlay.getData()
        
        if compression == 'Yes':
            cv2.imwrite(name,to_save,[cv2.IMWRITE_JPEG_QUALITY, 20])
        else:
            cv2.imwrite(name,to_save)

        
    