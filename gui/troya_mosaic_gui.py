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
        
        idx_row = 0
        
        button_main_photo = ttk.Button(mainwindow, text='Añadir Foto Principal', command=self.OpenMain)
        button_main_photo.grid(column=0, row=idx_row, columnspan=4, pady=5, sticky=tk.NSEW)
        idx_row+=1
        
        self.button_rot_left = ttk.Button(mainwindow, text='⟲', command=lambda: self.RotateCurrent(mode='left',new_width=height.get(),n_photos=nrow.get()), state=tk.DISABLED)
        self.button_rot_left.grid(column=0, row=idx_row, columnspan=2, sticky=tk.NSEW)
        self.button_rot_right = ttk.Button(mainwindow, text='⟳', command=lambda: self.RotateCurrent(mode='right',new_width=height.get(),n_photos=nrow.get()), state=tk.DISABLED)
        self.button_rot_right.grid(column=2, row=idx_row, columnspan=2, sticky=tk.NSEW)
        idx_row+=1
        
        
        ttk.Separator(mainwindow).grid(column=0, row=idx_row, columnspan=4, pady=10, sticky=tk.NSEW)
        idx_row+=1
        
        
        ttk.Label(mainwindow,text='Tamaño Resultado').grid(column=0, row=idx_row, columnspan=4)
        idx_row+=1
        
        height = tk.IntVar()
        ttk.Label(mainwindow,text='Alto').grid(column=1, row=idx_row, pady=2)
        self.height_entry = ttk.Entry(mainwindow, state=tk.DISABLED, width=10, textvariable=height)
        self.height_entry.grid(column=2, row=idx_row, pady=2)
        idx_row+=1
        
        width = tk.IntVar()
        ttk.Label(mainwindow,text='Ancho').grid(column=1, row=idx_row, pady=2)
        self.width_entry = ttk.Entry(mainwindow, width=10, textvariable=width, validatecommand=lambda: self.callback_size(width.get(), ncol.get()), validate='focusout')
        self.width_entry.grid(column=2, row=idx_row, pady=2)
        idx_row+=1
        
        ttk.Label(mainwindow,text='Número de Mosaicos').grid(column=0, row=idx_row, columnspan=4, pady=(15,2))
        idx_row+=1
        
        nrow = tk.IntVar()
        ttk.Label(mainwindow,text='Nº Filas').grid(column=1, row=idx_row, pady=2)
        self.nrow_entry = ttk.Entry(mainwindow, state=tk.DISABLED, width=10, textvariable=nrow)
        self.nrow_entry.grid(column=2, row=idx_row, pady=2)
        idx_row+=1
        
        ncol = tk.IntVar()
        ttk.Label(mainwindow,text='Nº Columnas').grid(column=1, row=idx_row, pady=2)
        self.ncol_entry = ttk.Entry(mainwindow, width=10, textvariable=ncol, validatecommand=lambda: self.callback_size(width.get(), ncol.get()), validate='focusout')
        self.ncol_entry.grid(column=2, row=idx_row, pady=2)
        idx_row+=1
        
        
        ttk.Separator(mainwindow).grid(column=0, row=idx_row, columnspan=4, pady=10, sticky=tk.NSEW)
        idx_row+=1
        
        
        button_tiles = tk.Button(mainwindow, text='Añadir Mosaicos', command=self.OpenTiles)
        button_tiles.grid(column=0, row=idx_row, columnspan=4, sticky=tk.NSEW)
        idx_row+=1
        button_dir = tk.Button(mainwindow, text='Añadir Carpeta', command=self.OpenDir)
        button_dir.grid(column=0, row=idx_row, columnspan=4, pady=(0,2), sticky=tk.NSEW)
        idx_row+=1
        
        self.n_anyadidas = ttk.Label(mainwindow, text='0 fotos añadidas')
        self.n_anyadidas.grid(column=1, row=idx_row, columnspan=2, pady=2)
        idx_row+=1
        
        
        ttk.Separator(mainwindow).grid(column=0, row=idx_row, columnspan=4, pady=10, sticky=tk.NSEW)
        idx_row+=1
        
        
        dist_rep = tk.IntVar()
        ttk.Label(mainwindow,text='Dist. sin repetir').grid(column=1, row=idx_row, pady=2)
        ttk.Entry(mainwindow,width=10, textvariable=dist_rep).grid(column=2, row=idx_row, pady=2)
        idx_row+=1
        
        
        button_generate = ttk.Button(mainwindow, text='Generar Resultado', command=lambda: self.GenerateResult(ncol.get(),width.get(),dist_rep.get()))
        button_generate.grid(column=0, row=idx_row, columnspan=4, pady=2, sticky=tk.NSEW)
        idx_row+=1
        
        
        ttk.Separator(mainwindow).grid(column=0, row=idx_row, columnspan=4, pady=10, sticky=tk.NSEW)
        idx_row+=1
        
        
        ttk.Label(mainwindow,text='Transparencia de la imagen principal').grid(column=0,row=idx_row,columnspan=4,pady=2)
        idx_row+=1
        
        self.alpha=tk.DoubleVar()
        self.alpha=0.0
        self.alpha_entry = ttk.Entry(mainwindow, textvariable=self.alpha, width=10, justify='center', state=tk.DISABLED)
        self.alpha_entry.insert(tk.END, str(self.alpha))
        self.alpha_entry.grid(column=0, row=idx_row, columnspan=2, rowspan=2)
        
        self.button_increment = ttk.Button(mainwindow, text='+', width=2, command=self.incrementAlpha, state=tk.DISABLED)
        self.button_increment.grid(column=2, row=idx_row, columnspan=2)
        idx_row+=1
        self.button_decrement = ttk.Button(mainwindow, text='–', width=2, command=self.decrementAlpha, state=tk.DISABLED)
        self.button_decrement.grid(column=2, row=idx_row, columnspan=2)
        idx_row+=1
        
        button_save = ttk.Button(mainwindow, text='Guardar', command=self.SaveResult)
        button_save.grid(column=0, row=idx_row, columnspan=4, pady=10, sticky=tk.NSEW)
        
        
        self.fig, self.ax = plt.subplots(1,1,figsize=(7,5))
        self.ax.axis('off')        
        self.canvas_result = FigureCanvasTkAgg(self.fig, master=mainwindow)        
        self.canvas_result.get_tk_widget().grid(column=5, row=0, rowspan=idx_row+1, columnspan=16, padx=15, pady=15)
   
     
        mainwindow.config(height=200, width=400)
        mainwindow.pack(side='top',padx=10,pady=10)
        
        # Main widget
        self.mainwindow = mainwindow
    
        
    
    def OpenMain(self):
        main_photo_name = tk.filedialog.askopenfilename(initialdir='.', title='Selecciona la foto principal', filetypes=(('Archivos de Imagen', '*.png *.jpg'),('Todos los archivos','*.*')))
        
        if main_photo_name:
            self.__troya.addMainImg(main_photo_name)
            
            self.button_rot_left.config(state=tk.NORMAL)
            self.button_rot_right.config(state=tk.NORMAL)
            
            self.callback_size(width=self.__troya.getMainImg().shape[1],n_photos_width=75)
            
            self.alpha_entry.config(state=tk.DISABLED)
            self.button_increment.config(state=tk.DISABLED)
            self.button_decrement.config(state=tk.DISABLED)
            
            self.alpha=0.0
            self.alpha_entry.delete(0,tk.END)
            self.alpha_entry.insert(0,self.alpha)
            
            self.plotInCanvas()
            
    def RotateCurrent(self, mode, new_width, n_photos):
        if mode == 'left':
            self.__troya.rotate_image(orient='left')
        elif mode ==  'right':
            self.__troya.rotate_image(orient='right')
        
        self.callback_size(width=new_width, n_photos_width=n_photos)
        self.plotInCanvas()
        
    def callback_size(self, width, n_photos_width):
        if not self.__troya.getMainImg().isEmpty():
            if width % n_photos_width != 0:
                width -= width % n_photos_width
            
            tile_size = int(width/n_photos_width)
            
            proportion = self.__troya.getMainImg().shape[0]/self.__troya.getMainImg().shape[1]
            height = int(width*proportion)
            n_photos_height = int(height/tile_size)
            
            if n_photos_height == 0:
                n_photos_height=1
            
            height = n_photos_height*tile_size
            
            self.height_entry.config(state=tk.NORMAL)
            self.height_entry.delete(0,tk.END)
            self.height_entry.insert(0,str(height))
            self.height_entry.config(state=tk.DISABLED)
            self.width_entry.delete(0,tk.END)
            self.width_entry.insert(0,str(width))
            
            self.nrow_entry.config(state=tk.NORMAL)
            self.nrow_entry.delete(0,tk.END)
            self.nrow_entry.insert(0,str(n_photos_height))
            self.nrow_entry.config(state=tk.DISABLED)
            self.ncol_entry.delete(0,tk.END)
            self.ncol_entry.insert(0,str(n_photos_width))
            
        return True
            
    
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
        
    def GenerateResult(self, ncol, width, dist):
        if self.__troya.getMainImg().isEmpty():
            tk.messagebox.showinfo(title='Información', message='Carga antes una imagen principal!')
        elif len(self.__troya.getTiles()) == 0:
            tk.messagebox.showinfo(title='Información', message='Carga antes los mosaicos!')
        else:
            success = self.__troya.generate_by_color(n_photos_width=int(ncol),width=int(width),dist_rep=dist)
            
            if success:
                self.plotInCanvas()
            
                self.alpha_entry.config(state=tk.NORMAL)
                self.button_increment.config(state=tk.NORMAL)
                self.button_decrement.config(state=tk.NORMAL)
                
                self.alpha=0.0
                self.alpha_entry.delete(0,tk.END)
                self.alpha_entry.insert(0,self.alpha)
                
                tk.messagebox.showinfo(title='Información', message='Imagen generada!')
            else:
                tk.messagebox.showinfo(title='Información', message='No se puede generar la imagen con una separación de ' +str(dist)+ ' casillas sin repeticiones.')
        
        
    def incrementAlpha(self):
        if self.alpha < 10:
            self.alpha+=1
            self.alpha_entry.delete(0,tk.END)
            self.alpha_entry.insert(0,self.alpha/10)
            
            self.__troya.maskOverlay(self.alpha/10)
            
            self.plotInCanvas()
    
    def decrementAlpha(self):
        if self.alpha > 0:
            self.alpha-=1
            self.alpha_entry.delete(0,tk.END)
            self.alpha_entry.insert(0,self.alpha/10)
            
            self.__troya.maskOverlay(self.alpha/10)
            
            self.plotInCanvas()
        
    def SaveResult(self):
        where_to_save = tk.filedialog.asksaveasfilename(initialdir='.', title='Selecciona donde guardar el resultado',filetypes=(('Archivos PNG', '*.png'),('Archivos JPG', '*.jpg'),('Todos los archivos','*.*')))
        if where_to_save:
            self.__troya.saveResult(where_to_save, compression=False, overlay=True)
    
    def plotInCanvas(self):
        toplot = self.__troya.getOverlay().copy()
        
        plot_proportion = toplot.shape[0]/toplot.shape[1]
        
        if plot_proportion >= 1:
            plot_height = 800
            plot_width = int(800/plot_proportion)
        else:
            plot_width = 800
            plot_height = int(800*plot_proportion)
            
        toplot.resize_image(plot_width,plot_height)
        
        self.ax.imshow(toplot[:,:,::-1])
        self.canvas_result.draw()
        
    
    def openInfoWindow(self, info): 
        self.infoWindow = tk.Toplevel(self.mainwindow)
        self.infoWindow.title("Información")
        self.infoWindow.config(height=100,width=300)
        ttk.Label(self.infoWindow, text=info).pack()
        
    def closeInfoWindow(self):
        self.infoWindow.destroy()
            
    def run(self):
        self.mainwindow.mainloop()