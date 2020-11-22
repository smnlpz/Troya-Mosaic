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
        button_main_photo.grid(column=0, row=0, columnspan=4, pady=5, sticky=tk.NSEW)
        
        ttk.Separator(mainwindow).grid(column=0, row=1, columnspan=4, pady=10, sticky=tk.NSEW)
        
        ttk.Label(mainwindow,text='Tamaño Resultado').grid(column=0, row=2, columnspan=4)
        
        ttk.Label(mainwindow,text='Alto',state=tk.DISABLED).grid(column=1, row=3, pady=2)
        height = ttk.Entry(mainwindow, state=tk.DISABLED, width=10)
        height.grid(column=2, row=3, pady=2)
        
        width = tk.IntVar()
        ttk.Label(mainwindow,text='Ancho').grid(column=1, row=4, pady=2)
        self.width_entry = ttk.Entry(mainwindow,width=10, textvariable=width)
        self.width_entry.grid(column=2, row=4, pady=2)
        
        ttk.Label(mainwindow,text='Número de Mosaicos').grid(column=0, row=5, columnspan=4, pady=(15,2))
        
        ttk.Label(mainwindow,text='Nº Filas',state=tk.DISABLED).grid(column=1, row=6, pady=2)
        nrow = ttk.Entry(mainwindow,state=tk.DISABLED,width=10)
        nrow.grid(column=2, row=6, pady=2)
        
        ncol = tk.IntVar()
        ttk.Label(mainwindow,text='Nº Columnas').grid(column=1, row=7, pady=2)
        self.ncol_entry = ttk.Entry(mainwindow,width=10, textvariable=ncol)
        self.ncol_entry.grid(column=2, row=7, pady=2)
        
        
        ttk.Separator(mainwindow).grid(column=0, row=8, columnspan=4, pady=10, sticky=tk.NSEW)
        
        
        button_tiles = tk.Button(mainwindow, text='Añadir Mosaicos', command=self.OpenTiles)
        button_tiles.grid(column=0, row=9, columnspan=4, sticky=tk.NSEW)
        button_dir = tk.Button(mainwindow, text='Añadir Carpeta', command=self.OpenDir)
        button_dir.grid(column=0, row=10, columnspan=4, pady=(0,2), sticky=tk.NSEW)
        
        
        self.n_anyadidas = ttk.Label(mainwindow, text='0 fotos añadidas')
        self.n_anyadidas.grid(column=1, row=11, columnspan=2, pady=2)
        
        
        ttk.Separator(mainwindow).grid(column=0, row=12, columnspan=4, pady=10, sticky=tk.NSEW)
        
        
        button_generate = ttk.Button(mainwindow, text='Generar Resultado', command=lambda: self.GenerateResult(ncol.get(),width.get()))
        button_generate.grid(column=0, row=13, columnspan=4, pady=2, sticky=tk.NSEW)
        
        
        ttk.Separator(mainwindow).grid(column=0, row=14, columnspan=4, pady=10, sticky=tk.NSEW)
        
        
        ttk.Label(mainwindow,text='Transparencia de la imagen principal').grid(column=0,row=15,columnspan=4,pady=2)
        
        self.alpha=tk.DoubleVar()
        self.alpha=0.0
        self.alpha_entry = ttk.Entry(mainwindow, textvariable=self.alpha, width=10, justify='center')
        self.alpha_entry.insert(tk.END, str(self.alpha))
        self.alpha_entry.grid(column=0, row=16, columnspan=2, rowspan=2)
        
        button_increment = ttk.Button(mainwindow, text='+', width=2, command=self.incrementAlpha)
        button_increment.grid(column=2, row=16, columnspan=2)
        button_decrement = ttk.Button(mainwindow, text='–', width=2, command=self.decrementAlpha)
        button_decrement.grid(column=2, row=17, columnspan=2)
        
        
        button_save = ttk.Button(mainwindow, text='Guardar', command=self.SaveResult)
        button_save.grid(column=0, row=18, columnspan=4, pady=10, sticky=tk.NSEW)
        
        
        self.fig, self.ax = plt.subplots(1,1,figsize=(7,5))
        self.ax.axis('off')        
        self.canvas_result = FigureCanvasTkAgg(self.fig, master=mainwindow)        
        self.canvas_result.get_tk_widget().grid(column=5, row=0, rowspan=19, columnspan=16, padx=15, pady=15)
   
     
        mainwindow.config(height=200, width=400)
        mainwindow.pack(side='top',padx=10,pady=10)
        
        # Main widget
        self.mainwindow = mainwindow
    
    def incrementAlpha(self):
        if self.alpha < 10:
            self.alpha+=1
            self.alpha_entry.delete(0,tk.END)
            self.alpha_entry.insert(0,self.alpha/10)
            
            self.__troya.maskOverlay(self.alpha/10)
            
            self.ax.imshow(self.__troya.getOverlay()[:,:,::-1])
    
            self.canvas_result.draw()
    
    def decrementAlpha(self):
        if self.alpha > 0:
            self.alpha-=1
            self.alpha_entry.delete(0,tk.END)
            self.alpha_entry.insert(0,self.alpha/10)
            
            self.__troya.maskOverlay(self.alpha/10)
            
            self.ax.imshow(self.__troya.getOverlay()[:,:,::-1])
    
            self.canvas_result.draw()
        
    
    def OpenMain(self):
        main_photo_name = tk.filedialog.askopenfilename(initialdir='.', title='Selecciona la foto principal', filetypes=(('Archivos de Imagen', '*.png *.jpg'),('Todos los archivos','*.*')))
        
        if main_photo_name:
            self.__troya.addMainImg(main_photo_name)
            
            self.width_entry.delete(0,tk.END)
            self.width_entry.insert(0,str(self.__troya.getMainImg().shape[1]))
            self.ncol_entry.delete(0,tk.END)
            self.ncol_entry.insert(0,str(75))
            
            self.ax.imshow(self.__troya.getMainImg()[:,:,::-1])
    
            self.canvas_result.draw()
    
    def OpenTiles(self):
        tiles_names = tk.filedialog.askopenfilenames(initialdir='.', title='Selecciona los mosaicos', filetypes=(('Archivos de Imagen', '*.png *.jpg'),('Todos los archivos','*.*')))
        
        if tiles_names:
            self.openInfoWindow('Cargando Mosaicos...')
            for tile in tiles_names:
                self.__troya.addTile(tile)
            
            self.closeInfoWindow()
            self.n_anyadidas.config(text=str(len(self.__troya.getTiles())) + ' fotos añadidas')
        
    def OpenDir(self):
        direct = tk.filedialog.askdirectory(initialdir='.', title='Selecciona la carpeta que contiene los mosaicos')
        
        if direct:
            self.__troya.addDirectory(direct)
            self.n_anyadidas.config(text=str(len(self.__troya.getTiles())) + ' fotos añadidas')
        
    def GenerateResult(self,ncol,width):        
        self.__troya.generate_by_color(n_photos_width=int(ncol),width=int(width))
        
        self.ax.imshow(self.__troya.getResult()[:,:,::-1])
        
        self.canvas_result.draw()
        
        self.alpha=0.0
        self.alpha_entry.delete(0,tk.END)
        self.alpha_entry.insert(0,self.alpha)
        
        tk.messagebox.showinfo(title='Información', message='Imagen generada!')
        
    def SaveResult(self):
        where_to_save = tk.filedialog.asksaveasfilename(initialdir='.', title='Selecciona donde guardar el resultado',filetypes=(('Archivos PNG', '*.png'),('Archivos JPG', '*.jpg'),('Todos los archivos','*.*')))
        if where_to_save:
            self.__troya.saveResult(where_to_save, compression=False, overlay=True)
    
    def openInfoWindow(self, info): 
        self.infoWindow = tk.Toplevel(self.mainwindow)
        self.infoWindow.title("Información")
        self.infoWindow.config(height=100,width=300)
        ttk.Label(self.infoWindow, text=info).pack()
        
    def closeInfoWindow(self):
        self.infoWindow.destroy()
            
    def run(self):
        self.mainwindow.mainloop()
        