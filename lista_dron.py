from nodo_dron import nodo_dron
from dron import dron
class lista_dron:
    def __init__(self):
        self.head = None
        self.drone_count = 0
        self.name = "" 
        self.tiempo =0
    def pasar_tiempo(self):
        self.tiempo += 1    
    def add_drone(self,dron):
        if self.head is None:
            self.head = nodo_dron(dron=dron)
            self.drone_count += 1
            return
        aux = self.head
        while aux.sig:
            aux = aux.sig
        aux.sig = nodo_dron(dron=dron)
        self.drone_count += 1
    def subir_dron(self,id):
        aux = self.head
        while aux:
            if aux.dron.id == id:
                aux.dron.heigth += 1
                return
            aux = aux.sig
    def bajar_dron(self,id):
        aux = self.head
        while aux:
            if aux.dron.id == id:
                aux.dron.heigth -= 1
                return
            aux = aux.sig
    def altura_dron(self,id):
        aux = self.head
        while aux:
            if aux.dron.id == id:
                return aux.dron.heigth
            aux = aux.sig
    def up(self,id):
        aux = self.head
        while aux:
            if aux.dron.id == id:
                aux.dron.status = "Subir"
                return
            aux = aux.sig
    def down(self,id):
        aux = self.head
        while aux:
            if aux.dron.id == id:
                aux.dron.status = "Bajar"
                return
            aux = aux.sig
    def wait(self):
        aux = self.head
        while aux:
            aux.dron.status = "Esperar"
            aux = aux.sig
    def print_list(self):
        if self.head is None:
            print("=====================================")
            print("Lista de drones vacia")
            print("=====================================")
            return
        print(self.name)
        print("=====================================")
        aux = self.head
        while aux != None:
            print(" Drone: ",aux.dron.id,"Status: ",aux.dron.status,"Heigth: ",aux.dron.heigth,"Info: ",aux.dron.info)
            aux = aux.sig
        print("=====================================")
        print("\n Total de drones: ",self.drone_count)
    
        
        
