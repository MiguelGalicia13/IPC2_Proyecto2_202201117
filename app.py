import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import xml.etree.ElementTree as ET
from dron import dron
from lista_dron import lista_dron
lista_dron_temporal=lista_dron()
archivo = None  # Reinicializa la variable archivo
dron_temporal = dron()
route= None
root = None
class ScrollText(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.text = tk.Text(
            self,
            bg="#f8f9fa",
            foreground="#343a40",
            insertbackground="#3b5bdb",
            selectbackground="blue",
            width=120,
            height=25,
            font=("Courier New", 13),
        )

        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.text.yview)
        self.text.configure(yscrollcommand=self.scrollbar.set)

        self.numberLines = TextLineNumbers(self, width=40, bg="#dee2e6")
        self.numberLines.attach(self.text)

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.numberLines.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
        self.text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.text.bind("<Key>", self.onPressDelay)
        self.text.bind("<Button-1>", self.numberLines.redraw)
        self.scrollbar.bind("<Button-1>", self.onScrollPress)
        self.text.bind("<MouseWheel>", self.onPressDelay)
        
    def onScrollPress(self, *args):
        self.scrollbar.bind("<B1-Motion>", self.numberLines.redraw)

    def onScrollRelease(self, *args):
        self.scrollbar.unbind("<B1-Motion>", self.numberLines.redraw)

    def onPressDelay(self, *args):
        self.after(2, self.numberLines.redraw)

    def get(self, *args, **kwargs):
        return self.text.get(*args, **kwargs)

    def insert(self, *args, **kwargs):
        return self.text.insert(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.text.delete(*args, **kwargs)

    def index(self, *args, **kwargs):
        return self.text.index(*args, **kwargs)

    def redraw(self):
        self.numberLines.redraw()

class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs, highlightthickness=0)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        """redraw line numbers"""
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True:
            dline = self.textwidget.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(
                2,
                y,
                anchor="nw",
                text=linenum,
                fill="#868e96",
                font=("Courier New", 13, "bold"),
            )
            i = self.textwidget.index("%s+1line" % i)

class Ventana(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Proyecto 1")
        self.geometry("1000x700")
        self.scroll = ScrollText(self)
        self.scroll.pack()
        self.after(200, self.scroll.redraw())
        self.menu = Menu(self)
        self.config(menu=self.menu)
        self.filemenu = Menu(self.menu)
        self.menu.add_cascade(label="Archivo", command=self.open_file)
        self.filemenu.add_command(label="Abrir Archivo")
        self.filemenu.add_command(label="Guardar Archivo")
        self.filemenu.add_command(label="Salir", command=self.destroy)
        
        self.filemenu.add_separator()
        self.menu.add_command(label="Analizar", command=self.analizar_drones)
        self.menu.add_command(label="Ver reporte")
        self.menu.add_command(label="Ver errores")
    def open_file(self):
        global root
        global route
        global archivo
        print("Cargando archivo")
        #? Se Carga el Archivo
        route = askopenfilename(filetypes=[("Archivo XML", "*.xml")])
        if not route:
            #? Mensaje de Error si no se carga el archivo
            tk.messagebox.showerror(title="Error", message="No se hay archivo seleccionado aun")
            return
        self.scroll.delete(1.0,tk.END)
        with open(route, "r") as input_file:
            text = input_file.read()
            self.scroll.insert(tk.END, text)
        self.title(f"Proyecto 2 - {route}")
        #? Parciar XML
        tree = ET.parse(route)
        root = tree.getroot()
        tk.messagebox.showinfo(title="Exito", message="Archivo cargado exitosamente")
    def analizar_drones(self):
        global route
        global root
        if not route:
            #? Mensaje de Error si no se carga el archivo
            tk.messagebox.showerror(title="Error", message="No se hay archivo seleccionado aun")
            return
        for listaDrones in root.findall("listaDrones"):
            for codigo_an in listaDrones.findall("dron"):
                codigo_dron = codigo_an.text
                nuevo_dron = dron(id=codigo_dron)
                lista_dron_temporal.add_drone(nuevo_dron)
        lista_dron_temporal.print_list()
        tk.messagebox.showinfo(title="Exito", message="Drones cargados exitosamente")
        for listaSistemasDrones in root.findall("listaSistemasDrones"):
            for sistema in listaSistemasDrones.findall("sistemaDrones"):
                nombre = sistema.get("nombre")
                lista_dron_temporal.name = nombre
                for alturamax in sistema.findall("alturaMaxima"):
                    altura_maxima = int(alturamax.text)
                for contenido in sistema.findall("contenido"):
                    for instruccion in contenido.findall("dron"):
                        id_dron = instruccion.text
                    for alturas in contenido.findall("alturas"):
                        for altura in alturas.findall("altura"):
                            altura_dr= altura.text
                            altura_dron = int(altura_dr)
                            if altura_dron <=altura_maxima:
                                if altura_dron > lista_dron_temporal.altura_dron(id_dron):
                                    for i in range(altura_dron):
                                        lista_dron_temporal.up(id_dron)
                                        lista_dron_temporal.print_list()
                                        lista_dron_temporal.subir_dron(id_dron)
                                        lista_dron_temporal.wait()
                                        lista_dron_temporal.print_list()
                                    
                                elif altura_dron < lista_dron_temporal.altura_dron(id_dron):
                                    lista_dron_temporal.down(id_dron)
                                    lista_dron_temporal.bajar_dron(id_dron)
                            else:
                                return tk.messagebox.showerror(title="Error", message="Altura maxima superada en instrucciones")   
                        
        print("=" * 50)
        print("Lista Analizada")
        print("=" * 50)
        lista_dron_temporal.print_list()



app = Ventana()
app.mainloop()

