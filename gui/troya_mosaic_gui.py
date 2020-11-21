import tkinter.filedialog
import tkinter as tk
import tkinter.ttk as ttk

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from scripts.troya_mosaic import TroyaMosaic

class TroyaMosaicGUI:
    def __init__(self, master=None):
        mainwindow = ttk.Frame(master)
        
        self.__troya = TroyaMosaic()
        
        button_main_photo = ttk.Button(mainwindow, text='Añadir Foto Principal', command=self.OpenMain)
        button_main_photo.grid(column=0, row=0, columnspan=4, pady=10, sticky=tk.NSEW)
        
        ttk.Separator(mainwindow).grid(column=0, row=1, columnspan=4, pady=20, sticky=tk.NSEW)
        
        ttk.Label(mainwindow,text='Tamaño Resultado').grid(column=0,row=2,columnspan=4)
        
        ttk.Label(mainwindow,text='Alto',state=tk.DISABLED).grid(column=1, row=3, pady=5)
        height = ttk.Entry(mainwindow,state=tk.DISABLED,width=10)
        height.grid(column=2, row=3, pady=5)
        
        width = tk.IntVar()
        ttk.Label(mainwindow,text='Ancho').grid(column=1, pady=5, row=4)
        self.width_entry = ttk.Entry(mainwindow,width=10, textvariable=width)
        self.width_entry.grid(column=2, pady=5, row=4)
        
        ttk.Label(mainwindow,text='Número de Mosaicos').grid(column=0,row=5,columnspan=4,pady=(20,5))
        
        ttk.Label(mainwindow,text='Nº Filas',state=tk.DISABLED).grid(column=1, pady=5, row=6)
        nrow = ttk.Entry(mainwindow,state=tk.DISABLED,width=10)
        nrow.grid(column=2, pady=5, row=6)
        
        ncol = tk.IntVar()
        ttk.Label(mainwindow,text='Nº Columnas').grid(column=1, pady=5, row=7)
        self.ncol_entry = ttk.Entry(mainwindow,width=10, textvariable=ncol)
        self.ncol_entry.grid(column=2, pady=5, row=7)
        
        
        ttk.Separator(mainwindow).grid(column=0, row=8, columnspan=4, pady=20, sticky=tk.NSEW)
        
        button_tiles = ttk.Button(mainwindow, text='Añadir Mosaicos', command=self.OpenTiles)
        button_tiles.grid(column=0, row=9, columnspan=4, pady=5, sticky=tk.NSEW)
        
        self.n_anyadidas = ttk.Label(mainwindow, text='0 fotos añadidas')
        self.n_anyadidas.grid(column=1, row=10, columnspan=2, pady=5)
        
        
        ttk.Separator(mainwindow).grid(column=0, row=11, columnspan=4, pady=20, sticky=tk.NSEW)
        
        
        button_generate = ttk.Button(mainwindow, text='Generar Resultado', command=lambda: self.GenerateResult(ncol.get(),width.get()))
        button_generate.grid(column=0, row=12, columnspan=4, pady=5, sticky=tk.NSEW)
        
        
        ttk.Separator(mainwindow).grid(column=0, row=13, columnspan=4, pady=20, sticky=tk.NSEW)
        
        
        ttk.Label(mainwindow,text='Nombre Resultado:').grid(column=0, row=14, columnspan=4)
        ttk.Label(mainwindow,text='./results/').grid(column=1, row=15, pady=5)
        
        self.name_result = ttk.Entry(mainwindow, width=10)
        self.name_result.grid(column=2, row=15, pady=5)
        
        button_save = ttk.Button(mainwindow, text='Guardar', command=lambda: self.SaveResult(self.name_result.get()))
        button_save.grid(column=0, row=16, columnspan=4, pady=5, sticky=tk.NSEW)
        
        self.fig, self.ax = plt.subplots(1,1,figsize=(10,6))
        self.ax.axis('off')        
        self.canvas_result = FigureCanvasTkAgg(self.fig, master=mainwindow)        
        self.canvas_result.get_tk_widget().grid(column=5, row=0, rowspan=16, columnspan=16, padx=20, pady=20)
   
     
        mainwindow.config(height='200', width='200')
        mainwindow.pack(side='top',padx=10,pady=10)
        
        # Main widget
        self.mainwindow = mainwindow
    
    def OpenMain(self):
        main_photo_name = tk.filedialog.askopenfilename(initialdir='.', title='Selecciona la foto principal', filetypes=(('Archivos de Imagen', '*.png *.jpg *.jpeg'),('Todos los archivos','*.*')))
        
        if main_photo_name != '':
            self.__troya.addMainImg(main_photo_name)
            
            self.width_entry.delete(0,tk.END)
            self.width_entry.insert(0,str(self.__troya.getMainImg().shape[0]))
            self.ncol_entry.delete(0,tk.END)
            self.ncol_entry.insert(0,str(75))
            
            self.ax.imshow(self.__troya.getMainImg()[:,:,::-1])
    
            self.canvas_result.draw()
    
    def OpenTiles(self):
        tiles_names = tk.filedialog.askopenfilenames(initialdir='.', title='Selecciona los mosaicos', filetypes=(('Archivos de Imagen', '*.png *.jpg *.jpeg'),('Todos los archivos','*.*')))
        
        for tile in tiles_names:
            self.__troya.addTile(tile)
        
        self.n_anyadidas.config(text=str(len(self.__troya.getTiles())) + ' fotos añadidas')
        
    def GenerateResult(self,ncol,width):
        self.__troya.generate_by_color(n_photos_width=int(ncol),width=int(width))
        
        self.ax.imshow(self.__troya.getResult()[:,:,::-1])
        
        self.canvas_result.draw()
        
    def SaveResult(self, name):
        self.__troya.saveResult(name, compression=False, overlay=False)
        
    
    
    def callback(self):
        #self.ncol.delete(0,tk.END)
        self.ncol.insert(tk.END,'e')
        print(self.nfil.get())
    
    def computeLaplace(self,b_error,check,check_value):
        self.textWindow.delete('1.0','end')
        self.textWindow.insert('end','Adios! (Buscar)')
    
    def computeError(self):
        # Comprobamos el error
        self.textWindow.delete('1.0','end')
        self.textWindow.insert('end','ERROR!')
    
    def plot(self,check_0,check_1,checkbuttons):
        self.textWindow.delete('1.0','end')
        self.textWindow.insert('end','PLOT!')
    
    def run(self):
        self.mainwindow.mainloop()
        