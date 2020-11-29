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
    __main_img = LargeImage()
    __generated = LargeImage()
    __colors_matrix = LargeImage()
    __final_result = LargeImage()
    
    def __init__(self,img_name=None,directory_name=None):
        if img_name is not None:
            self.addMainImg(img_name)
        
        if directory_name is not None:
            self.addDirectory(directory_name)
    
    def getTiles(self):
        return self.__tiles
    
    def getMainImg(self):
        return self.__main_img
    
    def getGenerated(self):
        return self.__generated
    
    def getColorsMatrix(self):
        return self.__colors_matrix
    
    def getFinalResult(self):
        return self.__final_result
    
    def addMainImg(self,main_name):
        print('Cargando imagen ' + main_name + ' ...\n')
        self.__main_img = LargeImage(cv2.imread(main_name, cv2.IMREAD_UNCHANGED))
        self.__generated = self.__main_img.copy()
        self.__colors_matrix = self.__main_img.copy()
        self.__final_result = self.__main_img.copy()
    
    def addTile(self,tile_name):
        img = cv2.imread(tile_name,cv2.IMREAD_UNCHANGED)
        if img is not None:
            self.__tiles.append(Tile(img))
    
    def deleteTiles(self):
        self.__tiles = []
            
    def addDirectory(self,directory_name):
        print('Cargando directorio ' + directory_name + '...\n')
        for filename in os.listdir(directory_name):
            self.addTile(os.path.join(directory_name,filename))
    
    @staticmethod
    def find_nearest(tiles, cuad, diffType):
        dists = np.array([diffType(tile,cuad) for tile in tiles])
        idx = dists.argmin()
        
        return idx, dists[idx]
    
    def adjustValues(self,width,n_photos_width):
        if width > 0 and n_photos_width > 0:
            if width % n_photos_width != 0:
                width -= width % n_photos_width
            
            tile_size = int(width/n_photos_width)
            
            proportion = self.__main_img.shape[0]/self.__main_img.shape[1]
            height = int(width*proportion)
            n_photos_height = int(height/tile_size)
            
            if n_photos_height == 0:
                n_photos_height = 1
            
            height = n_photos_height*tile_size
            
            return True, height, width, n_photos_height, n_photos_width, tile_size
        else:
            return False, 0, width, 0, n_photos_width, 0
        
    
    @staticmethod
    def checkEnt(idx_i,idx_j,matrix,dist=1):
        forbidden = []
        for i in range(idx_i-dist,idx_i+dist+1):
            for j in range(idx_j-dist,idx_j+dist+1):
                if (i<0 or i>=matrix.shape[0]) or (j<0 or j>=matrix.shape[1]) or (idx_i==i and idx_j==j):
                    continue
                forbidden.append(matrix[i,j])
                
        return forbidden
    
    def generate_by_color(self, n_photos_width, width, dist_rep=0, mostCommon=Tile.mostCommon_Average, redu=1):
        if width < n_photos_width:
            print('El ancho ha de ser mayor que el número de columnas')
            return False
        
        success, height, width, n_photos_height, n_photos_width, tile_size = self.adjustValues(width, n_photos_width)
        
        if not success:
            if width <= 0:
                print('El ancho ha de ser mayor que 0')
            if n_photos_width <= 0:
                print('El número de columnas ha de ser mayor que 0')
            return False
        
        self.__generated = self.__main_img.copy()
        self.__generated.resize_image(width,height)
        self.__colors_matrix = self.__generated.copy()
        
        mosaic_imgs = [tile.copy() for tile in self.__tiles]
        
        for i in range(len(mosaic_imgs)):
            mosaic_imgs[i].resize_image(tile_size,tile_size)
            mostCommon(mosaic_imgs[i],redu=redu)

        print(str(width) + ' píxeles de ancho y ' + str(n_photos_width) + ' fotos.')
        print(str(height) + ' píxeles de alto y ' + str(n_photos_height) + ' fotos.')

        print('Generando resultado...\n')
        
        if dist_rep < 0:
            dist_rep = 0
            
        used_matrix = -np.ones([n_photos_height,n_photos_width],dtype=np.int)
        
        for i in range(n_photos_height):
            for j in range(n_photos_width):
                if dist_rep == 0:
                    useful_mosaic = mosaic_imgs
                else:
                    forbidden = TroyaMosaic.checkEnt(i,j,used_matrix,dist_rep)
                    useful_mosaic = [elem for index, elem in enumerate(mosaic_imgs) if index not in forbidden]
                
                if not useful_mosaic:
                    print('No se puede generar la imagen con una separación de ' +str(dist_rep)+ ' casillas sin repeticiones.\n')
                    self.__generated = self.__main_img.copy()
                    return False
                
                cuadradito = Tile(self.__generated[i*tile_size:(i+1)*tile_size,j*tile_size:(j+1)*tile_size])
                mostCommon(cuadradito,redu=redu,n=1)
                idx, _ = TroyaMosaic.find_nearest(useful_mosaic,cuadradito,Tile.getDiff_by_color)
                
                self.__generated[i*tile_size:(i+1)*tile_size,j*tile_size:(j+1)*tile_size] = useful_mosaic[idx].getData()
                self.__colors_matrix[i*tile_size:(i+1)*tile_size,j*tile_size:(j+1)*tile_size] = cuadradito.getColor()
                
                if dist_rep == 0:
                    used_matrix[i,j] = idx
                else:
                    used_matrix[i,j] = next(k for k, elem in enumerate(mosaic_imgs) if (elem.getColor() == useful_mosaic[idx].getColor()).all())
        
        
        self.__final_result = self.__generated.copy()
        
        print('Done!\n')
        return True
        
    
    def rotate_image(self,orient):
        if orient ==  'left':
            self.__main_img.rotate_image(orient='left')
            self.__generated.rotate_image(orient='left')
            self.__colors_matrix.rotate_image(orient='left')
            self.__final_result.rotate_image(orient='left')
        elif orient == 'right':
            self.__main_img.rotate_image(orient='right')
            self.__generated.rotate_image(orient='right')
            self.__colors_matrix.rotate_image(orient='right')
            self.__final_result.rotate_image(orient='right')
    
    def setMask(self,alpha_colorized,alpha_overlay):
        colorized = LargeImage(cv2.addWeighted(self.__generated.getData(), 1-alpha_colorized, self.__colors_matrix.getData(), alpha_colorized, 0))
        
        resized = self.__main_img.copy()
        resized.resize_image(self.__generated.shape[1],self.__generated.shape[0])
        
        self.__final_result = LargeImage(cv2.addWeighted(colorized.getData(), 1-alpha_overlay, resized.getData(), alpha_overlay, 0))
    
    def plot(self,mode='cv2',img='final_result'):
        if img == 'main':
            self.__main_img.plot(mode=mode)
        elif img == 'generated':
            self.__generated.plot(mode=mode)
        elif img == 'colors_matrix':
            self.__colors_matrix.plot(mode=mode)
        elif img == 'final_result':
            self.__final_result.plot(mode=mode)
            
        
    def saveResult(self,name,compression=True):
        print('Guardando imagen '+ name + ' ...\n')
        
        to_save = self.__final_result.getData()

        if compression:
            cv2.imwrite(name,to_save,[cv2.IMWRITE_JPEG_QUALITY, 20])
        else:
            cv2.imwrite(name,to_save)
            
        print('Done!\n')

        
    