#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 11:51:34 2020

@author: simon
"""

from scripts.troya_mosaic import TroyaMosaic

import sys
import time


def main():
    if len(sys.argv) != 7:
        if len(sys.argv) > 1 and sys.argv[1] == '-h':
            print('Uso del programa:\npython3 run.py <img_principal> <directorio_mosaicos> <dist_rep> <n_imgs_col> <ancho_result> <nombre_result>\n')
            return
        if len(sys.argv) < 7:
            print('Faltan argumentos para el programa. Use -h para obtener ayuda.\n')
            return
    
    print('\n######################################\n')
    mosaic = TroyaMosaic(sys.argv[1],sys.argv[2])
    
    start_time = time.time()
    
    result = mosaic.generate_by_color(n_photos_width=int(sys.argv[4]),width=int(sys.argv[5]),dist_rep=int(sys.argv[3]))

    print("--- %s seconds ---" % (time.time() - start_time))
    
    if result:    
        mosaic.saveResult(sys.argv[6], compression=True)
        mosaic.setMask(alpha_overlay=0.25, alpha_colorized=0)
        mosaic.saveResult(sys.argv[6]+'_overlay.jpg', compression=True)
        
    print('Fin!\n')
    print('######################################\n')
    
if __name__ == "__main__":
    main()
   
