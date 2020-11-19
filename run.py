#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 11:51:34 2020

@author: simon
"""

from scripts.troya_mosaic import TroyaMosaic
from scripts.tile import Tile

import sys
import time


def main():
    if len(sys.argv) != 6:
        if len(sys.argv) > 1 and sys.argv[1] == '-h':
            print('Uso del programa:\npython3 run.py <img_principal> <directorio_mosaicos> <n_imgs_col> <ancho_result> <nombre_result>\n')
            return
        if len(sys.argv) < 6:
            print('Faltan argumentos para el programa. Use -h para obtener ayuda.\n')
            return
    
    print('\n######################################\n')
    mosaic = TroyaMosaic(sys.argv[1],sys.argv[2])
    
    start_time = time.time()
    
    mosaic.generate_by_color(n_photos_width=int(sys.argv[3]),width=int(sys.argv[4]))
    #mosaic.generate_by_pixel(int(sys.argv[3]))
    
    print("--- %s seconds ---" % (time.time() - start_time))
    
    mosaic.maskOverlay(0.25)
    #mosaic.plotResult(mode='cv2')
    
    mosaic.saveResult(sys.argv[5])
    mosaic.saveResult(sys.argv[5] + '_overlay.jpg',overlay=True)
    
    print('Fin!\n')
    print('######################################\n')
    
if __name__ == "__main__":
    main()
   
