from nodo_dron import nodo_dron
from dron import dron
import sys
import os
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import *
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
    def mostrar_drones(self):
        aux = self.head
        while aux:
            tk.messagebox.showinfo(title="Drones", message="Dron: "+str(aux.dron.id)+" Altura: "+str(aux.dron.heigth)+" Info: "+str(aux.dron.info))
            aux = aux.sig
    def up(self,id):
        aux = self.head
        while aux:
            if aux.dron.id == id:
                aux.dron.status = "Subir"
                return
            aux = aux.sig
    def light(self,id):
        aux = self.head
        while aux:
            if aux.dron.id == id:
                aux.dron.status = "Luz encendida"
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
        print("="*60)
        aux = self.head
        while aux != None:
            print(" Drone: ",aux.dron.id,"Status: ",aux.dron.status,"Heigth: ",aux.dron.heigth,"Info: ",aux.dron.info)
            aux = aux.sig
        print("="*60)
        print("\n Total de drones: ",self.drone_count)
    def add_data(self,id,info):
        aux = self.head
        while aux:
            if aux.dron.id == id:
                aux.dron.info = info
                return
            aux = aux.sig
    def is_empty(self):
        if self.head == None:
            return True
        return False
    def get_tiempo(self):
        return self.tiempo
    
    def graficar(self,h_max):
        f = open('IPC2_Proyecto2_202201117/aa.dot','w+')
        texto="digraph G {\nnode [shape=square];\nlabel=\"Sistema de Drones\";\nsome_node [\nlabel=<\n<table border=\"0\" cellborder=\"1\" cellspacing=\"1\" width=\"100%\" height=\"100%\">\n"
        texto+="<tr>\n"
        aux = self.head
        a = 0
        while aux!=None:
            if a == 0:
                texto+="<td bgcolor=\"yellow\" width=\"10\" height=\"10\" > Altura </td>\n"
                a = 1
            texto+="<td bgcolor=\"yellow\" width=\"10\" height=\"10\" >"+str(aux.dron.id)+"</td>\n"
            aux = aux.sig
        texto+="</tr>\n"
        for i in range(1, h_max + 1):
            texto+="<tr>\n"
            texto+="<td bgcolor=\"yellow\" width=\"10\" height=\"10\" >"+str(i)+"</td>\n"
            for j in range(1, self.drone_count + 1):
                texto+="<td bgcolor= \"white\" width=\"10\" height=\"10\">"+"</td>\n"
            texto+="</tr>\n"
        texto+="</table>>\n];\n}"
        f.write(texto)
        f.close()
        os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin'
        os.system('dot -Tpng IPC2_Proyecto2_202201117/aa.dot -o IPC2_Proyecto2_202201117/Drones.png')
        print("Se ha generado la Grafica")
    def grafica2(self):
        aux = self.head
        f = open('IPC2_Proyecto2_202201117/bb.dot','w+')
        texto="digraph G {\nnode [shape=square];\nlabel=\"Info Drones\";\nsome_node [\nlabel=<\n<table border=\"0\" cellborder=\"1\" cellspacing=\"1\" width=\"100%\" height=\"100%\">\n"
        texto+="<tr>\n"
        texto+="<td bgcolor=\"yellow\" width=\"10\" height=\"10\"> \"ID\"</td>\n"
        while aux!=None:
            texto+="<td bgcolor=\"yellow\" width=\"10\" height=\"10\">"+str(aux.dron.id)+"</td>\n"
            aux = aux.sig
        texto+="</tr>\n"
        texto+="<tr>\n"
        aux = self.head
        texto+="<td bgcolor=\"yellow\" width=\"10\" height=\"10\"> Altura</td>\n"
        while aux!=None:
            texto+="<td bgcolor=\"white\" width=\"10\" height=\"10\">"+str(aux.dron.heigth)+"</td>\n"
            aux = aux.sig
        texto+="</tr>\n"
        texto+="<tr>\n"
        aux = self.head
        texto+="<td bgcolor=\"yellow\" width=\"10\" height=\"10\"> Coidgo</td>\n"
        while aux!=None:
            if aux.dron.info == None:
                texto+="<td bgcolor=\"white\" width=\"10\" height=\"10\">"+str(" ")+"</td>\n"
            else:
                texto+="<td bgcolor=\"white\" width=\"10\" height=\"10\">"+str(aux.dron.heigth)+"</td>\n"
            aux = aux.sig
        texto+="</tr>\n"
        texto+="</table>>\n];\n}"
        f.write(texto)
        f.close()
        os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin'
        os.system('dot -Tpng IPC2_Proyecto2_202201117/bb.dot -o IPC2_Proyecto2_202201117/info.png')
        print("Se ha generado la Grafica2")
    def archivo_salida(self):
        mis_drones = ET.Element("Respuesta")
        
