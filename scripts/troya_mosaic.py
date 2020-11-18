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
    
    
    def find_nearest(tiles, cuad):
        dists = np.array([tile.getDiff(cuad) for tile in tiles])
        idx = dists.argmin()
        
        return idx, tiles[idx].getColor()[0]
    
    def generate(self,n_photos,mostCommon,redu=1):
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
                idx, _ = TroyaMosaic.find_nearest(mosaic_imgs,cuadradito)
                self.__result[i:i+size_mosaic,j:j+size_mosaic] = mosaic_imgs[idx].getData()
                
        print('Done!\n')
    
    
    def plotResult(self,mode='cv2'):
        if mode == 'cv2':
            self.__result.plot()
        elif mode == 'plt':
            self.__result.plot_matplotlib()
            
    
    def saveResult(self,name,compression='Yes'):
        print('Guardando imagen '+ name + ' ...\n')
        if compression == 'Yes':
            cv2.imwrite(name,self.__result.getData(),[cv2.IMWRITE_JPEG_QUALITY, 20])
        else:
            cv2.imwrite(name,self.__result.getData())

        
    