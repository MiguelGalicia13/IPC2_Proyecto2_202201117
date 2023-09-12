from nodo_dron import nodo_dron
from dron import dron
class lista_dron:
    def __init__(self):
        self.head = None
        self.drone_count = 0
    def add_drone(self,dron):
        if self.head is None:
            self.head = nodo_dron(drone=dron)
            self.drone_count += 1
            return
        aux = self.head
        while aux.sig:
            aux = aux.sig
        aux.sig = nodo_dron(drone=dron)
        self.drone_count += 1
    def print_list(self):
        if self.head is None:
            print("=====================================")
            print("Lista de drones vacia")
            print("=====================================")
            return
        print("\n Total de drones: ",self.drone_count)
        print("=====================================")
        aux = self.head
        while aux != None:
            print(" Drone: ",aux.drone.id,"Status: ",aux.drone.status,"Heigth: ",aux.drone.heigth,"Info: ",aux.drone.info)
            aux = aux.sig
        print("=====================================")
    
        
        
