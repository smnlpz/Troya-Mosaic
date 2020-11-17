#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 19:35:22 2020

@author: simon
"""

import numpy as np
import cv2
import os

from scripts.large_image import LargeImage
from scripts.tile import Tile

'''
Carga y tratamiento de la imagen
'''
def load_main(name):
    return LargeImage(cv2.imread(name, cv2.IMREAD_UNCHANGED))
    

def load_tiles(folder):
    tiles = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename),cv2.IMREAD_UNCHANGED)
        if img is not None:
            tiles.append(Tile(img))
    return tiles




'''
Dividir la imagen y buscar la más similar
'''
def find_nearest(tiles, cuad):
    dists = np.array([tile.getDiff(cuad) for tile in tiles])
    idx = dists.argmin()
    
    return tiles[idx].getColor[0]

def find_idx_nearest(tiles, cuad):
    dists = np.array([tile.getDiff(cuad) for tile in tiles])
    idx = dists.argmin()
    
    return idx

# Función principal
def TroyaMosaic(img,mosaic_imgs,n_photos,mostCommon,redu=1):
    result = img.copy()
    
    height = result.shape[0]
    width = result.shape[1]
    
    size_mosaic = int(height/n_photos)
    
    for i in range(len(mosaic_imgs)):
        mosaic_imgs[i].resize_image(size_mosaic,size_mosaic)
        mostCommon(mosaic_imgs[i],redu=redu)
    
    
    for i in np.arange(0,height,size_mosaic):
        for j in np.arange(0,width,size_mosaic):
            cuadradito = Tile(result[i:i+size_mosaic,j:j+size_mosaic])
            mostCommon(cuadradito,redu=1,n=1)
            idx = find_idx_nearest(mosaic_imgs,cuadradito)
            result[i:i+size_mosaic,j:j+size_mosaic] = mosaic_imgs[idx].getData()
    
    return result
    


def main():
    main_img = load_main('./images/troyita.png')
    main_img.resize_image(2500,2500)
    
    mosaic_imgs = load_tiles('./images/mosaic/')
    
    result_Average = TroyaMosaic(main_img,mosaic_imgs,250,Tile.mostCommon_Average)
    result_PixelCount = TroyaMosaic(main_img,mosaic_imgs,250,Tile.mostCommon_PixelCount)
    result_AveragePixelCount = TroyaMosaic(main_img,mosaic_imgs,250,Tile.mostCommon_AveragePixelCount)
    #result_KMeans = TroyaMosaic(main_img,mosaic_imgs,250,mostCommon_KMeans)
    print("Done!\n")
    
    cv2.imwrite('results/average/average.jpg',result_Average.getData(),[cv2.IMWRITE_JPEG_QUALITY, 20])
    cv2.imwrite('results/redu_1/pixel_count.jpg',result_PixelCount.getData(),[cv2.IMWRITE_JPEG_QUALITY, 20])
    cv2.imwrite('results/redu_1/average_pixel_count.jpg',result_AveragePixelCount.getData(),[cv2.IMWRITE_JPEG_QUALITY, 20])
    #cv2.imwrite('results/kmeans/kmeans.jpeg',result_KMeans.getData(),[cv2.IMWRITE_JPEG_QUALITY, 20])
   

if __name__ == "__main__":
    main()
