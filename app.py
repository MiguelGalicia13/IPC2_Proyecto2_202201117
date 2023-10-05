import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfilename
from lista_alturas import lista_alturas
import xml.etree.ElementTree as ET
from dron import dron
from alturas import alturas
from lista_dron import lista_dron
lista_dron_temporal=lista_dron()
dron_temporal = dron()
alturas_temporal = alturas()
archivo = None  # Reinicializa la variable archivo
route= None
root = None
alt_max = 0
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
        self.menu.add_command(label="Archivo", command=self.open_file)
        self.config(menu=self.menu)
        self.filemenu = Menu(self.menu)
        self.menu.add_cascade(label="Gestor de Drones", menu=self.filemenu)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Analizar", command=self.analizar_drones)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Generar Grafica", command=self.graficar)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Mostrar Drones", command=self.mostrar)
        self.filemenu.add_separator()
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
        global alt_max
        lista_alturasI = lista_alturas()
        global route
        global root
        id_dr=""
        h_supuesta=""
        data=""
        composicion=""
        if not route:
            #? Mensaje de Error si no se carga el archivo
            tk.messagebox.showerror(title="Error", message="No se hay archivo seleccionado aun")
            return
        for listaDrones in root.findall("listaDrones"):
            for codigo_an in listaDrones.findall("dron"):
                codigo_dron = codigo_an.text
                nuevo_dron = dron(id=codigo_dron)
                lista_dron_temporal.add_drone(nuevo_dron)
        
        for listaSistemasDrones in root.findall("listaSistemasDrones"):
            for sistema in listaSistemasDrones.findall("sistemaDrones"):
                nombre = sistema.get("nombre")
                lista_dron_temporal.name = nombre
                for alturamax in sistema.findall("alturaMaxima"):
                    altura_maxima = int(alturamax.text)
                    alt_max = altura_maxima
                for n_drones in sistema.findall("cantidadDrones"):
                    numero_drones = int(n_drones.text)
                for contenido in sistema.findall("contenido"):
                    for dron_t in contenido.findall("dron"):
                            id_dr = dron_t.text
                            lista_alturasI.change_dron(id_dr)
                    for ht_alturas in contenido.findall("alturas"):
                        for ht_altura in ht_alturas.findall("altura"):
                            h_supuesta = ht_altura.get("valor")
                            dato = ht_altura.text
                            nueva_altura = alturas(h=h_supuesta,data=dato)
                            lista_alturasI.add_altura(nueva_altura)
        
        for listaMensajes_temp in root.findall("listaMensajes"):
            for mensaje in listaMensajes_temp.findall("Mensaje"):
                nombre_msj = mensaje.get("nombre")
                for sistema in mensaje.findall("sistemaDrones"):
                    nombre_sistema = sistema.text
                for instrucciones in mensaje.findall("instrucciones"):
                    for instruccion in instrucciones.findall("instruccion"):
                        id_dron = instruccion.get("dron")
                        altura_ob = instruccion.text
                        altura_objetivo = int(altura_ob)
                        if altura_objetivo<=altura_maxima:
                            #? Serie de instrucciones
                            if altura_objetivo>lista_dron_temporal.altura_dron(id_dron):
                                for i in range(altura_objetivo):
                                    print("t: ",lista_dron_temporal.get_tiempo())
                                    lista_dron_temporal.up(id_dron)
                                    lista_dron_temporal.print_list()
                                    lista_dron_temporal.subir_dron(id_dron)
                                    lista_dron_temporal.wait()
                                    if i == altura_objetivo-1:
                                        lista_dron_temporal.light(id_dron)
                                        lista_dron_temporal.print_list()
                                        lista_dron_temporal.wait()
                                    lista_dron_temporal.pasar_tiempo()
                            elif altura_objetivo==lista_dron_temporal.altura_dron(id_dron):
                                lista_dron_temporal.light(id_dron)
                                lista_dron_temporal.print_list()
                                lista_dron_temporal.wait()
        tk.messagebox.showinfo(title="Exito", message="Drones cargados exitosamente")
        lista_dron_temporal.print_list()
    def graficar(self):
        global route
        global root
        global alt_max
        if not route    :
            #? Mensaje de Error si no se carga el archivo
            tk.messagebox.showerror(title="Error", message="No se hay archivo seleccionado aun")
            return
        if lista_dron_temporal.is_empty():
            tk.messagebox.showerror(title="Error", message="No se ha realizado el analisis")
            return
        
        lista_dron_temporal.graficar(alt_max)
        lista_dron_temporal.grafica2()
        print("")
        print("=" * 100)
        print("Lista Analizada")
        lista_dron_temporal.print_list()
    def mostrar(self):
        global route
        global root
        global alt_max
        if not route    :
            #? Mensaje de Error si no se carga el archivo
            tk.messagebox.showerror(title="Error", message="No se hay archivo seleccionado aun")
            return
        if lista_dron_temporal.is_empty():
            tk.messagebox.showerror(title="Error", message="No se ha realizado el analisis")
            return
        lista_dron_temporal.mostrar_drones()


app = Ventana()
app.mainloop()

