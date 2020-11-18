#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 11:51:34 2020

@author: simon
"""

from scripts.troya_mosaic import TroyaMosaic
from scripts.tile import Tile

import sys


def main():
    if len(sys.argv) != 6:
        if len(sys.argv) > 1 and sys.argv[1] == '-h':
            print('Uso del programa:\npython3 run.py <img_principal> <directorio_mosaicos> <n_imgs_row> <tamaño_img_result> <nombre_result>\n')
            return
        if len(sys.argv) < 6:
            print('Faltan argumentos para el programa. Use -h para obtener ayuda.\n')
            return
    
    print('\n###################\n')
    mosaic = TroyaMosaic(sys.argv[1],sys.argv[2])
    mosaic.resize_main(int(sys.argv[4]),int(sys.argv[4]))
    mosaic.generate(int(sys.argv[3]),Tile.mostCommon_Average)
    mosaic.saveResult(sys.argv[5])
    
    print('Fin!\n')
    print('\n###################\n')
    
if __name__ == "__main__":
    main()
   