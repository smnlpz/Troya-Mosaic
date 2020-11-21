#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 13:31:19 2020

@author: simon
"""

import tkinter as tk
from gui.troya_mosaic_gui import TroyaMosaicGUI

def main():
    root = tk.Tk()
    root.title('Troya Mosaic')
    troya = TroyaMosaicGUI(root)
    troya.run()
    
if __name__ == '__main__':
    main()