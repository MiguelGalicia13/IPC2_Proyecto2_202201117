from nodo_alturas import nodo_altura
from alturas import alturas
class lista_alturas:
    def __init__(self):
        self.head = None
        self.drone = None
    def add_altura(self,h_alt):
        if self.head is None:
            self.head=nodo_altura(H_altura=h_alt)
            return
        aux = self.head
        while aux.sig:
            aux = aux.sig
        aux.sig = nodo_altura(H_altura=h_alt)
    def change_dron(self,dron):
        self.drone = dron
    def print_list(self):
        aux = self.head
        print("Dron: ",self.drone)
        while aux:
            print(aux.H_altura.h," ",aux.H_altura.data)
            aux = aux.sig