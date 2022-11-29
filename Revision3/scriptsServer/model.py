from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from agent import *
import json
import math
class Vertice:
    """Clase que define los vertices de los grafos"""
    def __init__(self,i):
        self.id=i
        self.vecinos=[]
        self.visitado=False
        self.padre=None
        self.distancia=float('inf')
    
    def agregarVecino(self,v,p):
        if v not in self.vecinos:
            self.vecinos.append([v,p])
    
class Grafica:
    """Clase que define los vertices de las graficas"""
    def __init__(self):
        self.vertices={}
        self.listaVertices=[]
    
    def agregarVertice(self,id):
        if id not in self.vertices:
            self.vertices[id]=Vertice(id)
            self.listaVertices.append(id)
    
    def agregarArista(self,a,b,p):
        if a in self.vertices and b in self.vertices:
            self.vertices[a].agregarVecino(b,p)
            self.vertices[b].agregarVecino(a,p)
            print("Vertice inicial: " + str(a))
            print("Vertice Final: " + str(b))
            print("Peso: " + str(p))
            
            
        
    def imprimirGrafica(self):
        for v in self.vertices:
            print("La distancia del vertice "+str(v)+" es "+ str(self.vertices[v].distancia)+" llegando desde "+str(self.vertices[v].padre))
            
    def camino(self,a,b):
        camino=[]
        actual=b
        while actual != None:
            camino.insert(0,actual)
            actual=self.vertices[actual].padre
        return [camino, self.vertices[b].distancia]
    
    def minimo(self,lista):
        if len(lista)>0:
            m= self.vertices[lista[0]].distancia
            v=lista[0]
            for e in lista:
                if m > self.vertices[e].distancia:
                    m=self.vertices[e].distancia
                    v=e
            return v
            
    def dijkstra(self,a):
        if a in self.vertices:
            self.vertices[a].distancia=0
            actual = a
            noVisitados=[]
            
            for v in self.vertices:
                if v != a:
                    self.vertices[v].distancia=float('inf')
                self.vertices[v].padre=None
                noVisitados.append(v)
            
            while len(noVisitados)>0:
                for vecino in self.vertices[actual].vecinos:
                    if self.vertices[vecino[0]].visitado==False:
                        if self.vertices[actual].distancia+vecino[1] < self.vertices[vecino[0]].distancia:
                            self.vertices[vecino[0]].distancia=self.vertices[actual].distancia+vecino[1]
                            self.vertices[vecino[0]].padre=actual
                
                self.vertices[actual].visitado==True
                noVisitados.remove(actual)
                
                actual =self.minimo(noVisitados)
            
        else:
            return False

class RandomModel(Model):
    """ 
    Creates a new model with random agents.
    Args:
        N: Number of agents in the simulation
    """
    def __init__(self, N):
        
        #rutas = Grafo(self.next_id,self)
        #rutas=Grafo()
        rutas=Grafica()
        #Lista completa
        listRoad=[]
                #Almacena todos los valores de x y y por separado
        listaX=[]
        listaY=[]
        #Almacena las distancias entre las intersecciones temporalmente para extraer el minimo
        subX=[]
        subY=[]
        #Almacena las posiciones de la misma con los mismos indices que las distancias
        posicionVer=[]
        posicionHor=[]
        #Almacena las conexiones
        conexionVer=[]
        conexionHor=[]
        conexionDes=[]
        #Lista con nombres intersecciones
        listInt=[]
        super().__init__()
        dataDictionary = json.load(open("mapDictionary.json"))

        self.destination_pos= []

        self.traffic_lights = []
        self.occupied=[]
        with open('2022_base.txt') as baseFile:
            lines = baseFile.readlines()
            self.width = len(lines[0])-1
            self.height = len(lines)
            print(f"width :{self.width}")
            print(f"height :{self.height}" )
            self.grid = MultiGrid(self.width, self.height, torus = False) 
            self.schedule = RandomActivation(self)

            for r, row in enumerate(lines):
                for c, col in enumerate(row):
                    """
                    Para las intersecciones generar simbolos nuevos y declararlos en el modelo y el txt 2022_base y en el json
                    """
                    if col in ["v", "^", ">", "<","$","&","%","*"]:
                        agent = Road(f"r_{r*self.width+c}", self, dataDictionary[col])
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        listRoad.append([agent.pos, agent.direction])
                        if col in ["$","&","%","*"]:
                            rutas.agregarVertice((c, self.height - r - 1))
                            listInt.append(dataDictionary[col])
                        
                    elif col in ["S", "s"]:
                        agent = Traffic_Light(f"tl_{r*self.width+c}", self, False if col == "S" else True, int(dataDictionary[col]))
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)
                        self.traffic_lights.append(agent)

                    elif col == "#":
                        agent = Obstacle(f"ob_{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))

                    elif col == "D":
                        agent = Destination(f"d_{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.destination_pos.append((c,self.height - r - 1))
                        rutas.agregarVertice((c, self.height - r - 1))
                        listInt.append("Destination")
                    
        #Lista nombre Intersecciones listInt

        for i in rutas.listaVertices:
            listaX.append(i[0])
            listaY.append(i[1])

        for i in range(len(rutas.listaVertices)):
            
            if listInt[i] == "UpLeft":
                for j in range(len(listaX)):
                    if rutas.listaVertices[i][0] == listaX[j]:
                        if listaY[j]-rutas.listaVertices[i][1] > 0:
                            subY.append(listaY[j]-rutas.listaVertices[i][1])
                            posicionVer.append((listaX[j],listaY[j]))
                            
                                                
                    elif rutas.listaVertices[i][1] == listaY[j]:
                        if rutas.listaVertices[i][0]-listaX[j] > 0:
                            subX.append(rutas.listaVertices[i][0]-listaX[j])
                            posicionHor.append((listaX[j],listaY[j]))
              
                if len(subY)>0:
                    if min(subY)>1:
                        for k in range(min(subY)):
                            
                            if [(rutas.listaVertices[i][0]+1,rutas.listaVertices[i][1]+k), "Destination"] in listRoad:
                                conexionDes.append((rutas.listaVertices[i],(rutas.listaVertices[i][0]+1,rutas.listaVertices[i][1]+k),k+1))
                                rutas.agregarArista(rutas.listaVertices[i],(rutas.listaVertices[i][0]+1,rutas.listaVertices[i][1]+k),k+1)
                                
                            elif [(rutas.listaVertices[i][0]-1,rutas.listaVertices[i][1]+k), "Destination"] in listRoad:
                                conexionDes.append((rutas.listaVertices[i],(rutas.listaVertices[i][0]-1,rutas.listaVertices[i][1]+k),k+1))
                                rutas.agregarArista(rutas.listaVertices[i],(rutas.listaVertices[i][0]-1,rutas.listaVertices[i][1]+k),k+1)
                            
                            elif [(rutas.listaVertices[i][0]+2,rutas.listaVertices[i][1]+k), "Destination"] in listRoad and [(rutas.listaVertices[i][0]+1,rutas.listaVertices[i][1]+k), "Up"] in listRoad:
                                conexionDes.append((rutas.listaVertices[i],(rutas.listaVertices[i][0]+1,rutas.listaVertices[i][1]+k),k+2))
                                rutas.agregarArista(rutas.listaVertices[i],(rutas.listaVertices[i][0]+1,rutas.listaVertices[i][1]+k),k+2)
                                
                            elif [(rutas.listaVertices[i][0]-2,rutas.listaVertices[i][1]+k), "Destination"] in listRoad and [(rutas.listaVertices[i][0]-1,rutas.listaVertices[i][1]+k), "Up"] in listRoad:
                                conexionDes.append((rutas.listaVertices[i],(rutas.listaVertices[i][0]-1,rutas.listaVertices[i][1]+k),k+2))
                                rutas.agregarArista(rutas.listaVertices[i],(rutas.listaVertices[i][0]-1,rutas.listaVertices[i][1]+k),k+2)
                
                if len(subX)>0:
                    if min(subX)>1:
                        for k in range(min(subX)):
                            
                            if [(rutas.listaVertices[i][0]-k,rutas.listaVertices[i][1]+1),"Destination"] in listRoad:
                                conexionDes.append((rutas.listaVertices[i],(rutas.listaVertices[i][0]-k,rutas.listaVertices[i][1]+1),k+1))
                                rutas.agregarArista(rutas.listaVertices[i],(rutas.listaVertices[i][0]-k,rutas.listaVertices[i][1]+1),k+1)
                                
                            elif [(rutas.listaVertices[i][0]-k,rutas.listaVertices[i][1]-1), "Destination"] in listRoad:
                                conexionDes.append((rutas.listaVertices[i],(rutas.listaVertices[i][0]-k,rutas.listaVertices[i][1]-1),k+1))
                                rutas.agregarArista(rutas.listaVertices[i],(rutas.listaVertices[i][0]-k,rutas.listaVertices[i][1]-1),k+1)
                                
                                
                            elif [(rutas.listaVertices[i][0]-k,rutas.listaVertices[i][1]+2),"Destination"] in listRoad and [(rutas.listaVertices[i][0]-k,rutas.listaVertices[i][1]+1),"Left"] in listRoad:
                                conexionDes.append((rutas.listaVertices[i],(rutas.listaVertices[i][0]-k,rutas.listaVertices[i][1]+2),k+2))
                                rutas.agregarArista(rutas.listaVertices[i],(rutas.listaVertices[i][0]-k,rutas.listaVertices[i][1]+2),k+2)
                                
                            elif [(rutas.listaVertices[i][0]-k,rutas.listaVertices[i][1]-2), "Destination"] in listRoad and [(rutas.listaVertices[i][0]-k,rutas.listaVertices[i][1]-1), "Left"] in listRoad:
                                conexionDes.append((rutas.listaVertices[i],(rutas.listaVertices[i][0]-k,rutas.listaVertices[i][1]-2),k+2))
                                rutas.agregarArista(rutas.listaVertices[i],(rutas.listaVertices[i][0]-k,rutas.listaVertices[i][1]-2),k+2)
                                
            if listInt[i] == "UpRight":
                for j in range(len(listaX)):
                    if rutas.listaVertices[i][0] == listaX[j]:
                        if listaY[j]-rutas.listaVertices[i][1] > 0:
                            subY.append(listaY[j]-rutas.listaVertices[i][1])
                            posicionVer.append((listaX[j],listaY[j]))
                            
                                       
                            
                    elif rutas.listaVertices[i][1] == listaY[j]:
                        if listaX[j]-rutas.listaVertices[i][0] > 0:
                            subX.append(listaX[j]-rutas.listaVertices[i][0])
                            posicionHor.append((listaX[j],listaY[j]))
                            
                      
                if len(subY)>0:
                    if min(subY)>1:
                        for k in range(min(subY)):
                            
                            if [(rutas.listaVertices[i][0]+1,rutas.listaVertices[i][1]+k), "Destination"] in listRoad:
                                conexionDes.append((rutas.listaVertices[i],(rutas.listaVertices[i][0]+1,rutas.listaVertices[i][1]+k),k+1))
                                rutas.agregarArista(rutas.listaVertices[i],(rutas.listaVertices[i][0]+1,rutas.listaVertices[i][1]+k),k+1)
                                
                            elif [(rutas.listaVertices[i][0]-1,rutas.listaVertices[i][1]+k), "Destination"] in listRoad:
                                conexionDes.append((rutas.listaVertices[i],(rutas.listaVertices[i][0]-1,rutas.listaVertices[i][1]+k),k+1))
                                rutas.agregarArista(rutas.listaVertices[i],(rutas.listaVertices[i][0]-1,rutas.listaVertices[i][1]+k),k+1)
                                
                            elif [(rutas.listaVertices[i][0]+2,rutas.listaVertices[i][1]+k), "Destination"] in listRoad and [(rutas.listaVertices[i][0]+1,rutas.listaVertices[i][1]+k), "Up"] in listRoad:
                                conexionDes.append((rutas.listaVertices[i],(rutas.listaVertices[i][0]+2,rutas.listaVertices[i][1]+k),k+2))
                                rutas.agregarArista(rutas.listaVertices[i],(rutas.listaVertices[i][0]+2,rutas.listaVertices[i][1]+k),k+2)
                                
                            elif [(rutas.listaVertices[i][0]-2,rutas.listaVertices[i][1]+k), "Destination"] in listRoad and [(rutas.listaVertices[i][0]-1,rutas.listaVertices[i][1]+k), "Up"] in listRoad:
                                conexionDes.append((rutas.listaVertices[i],(rutas.listaVertices[i][0]-2,rutas.listaVertices[i][1]+k),k+2))
                                rutas.agregarArista(rutas.listaVertices[i],(rutas.listaVertices[i][0]-2,rutas.listaVertices[i][1]+k),k+2)
                
                if len(subX)>0:
                    if min(subX)>1:
                        for k in range(min(subX)):
                            
                            if [(rutas.listaVertices[i][0]+k,rutas.listaVertices[i][1]+1),"Destination"] in listRoad:
                                conexionDes.append((rutas.listaVertices[i],(rutas.listaVertices[i][0]+k,rutas.listaVertices[i][1]+1),k+1))
                                rutas.agregarArista(rutas.listaVertices[i],(rutas.listaVertices[i][0]+k,rutas.listaVertices[i][1]+1),k+1)
                                
                            elif [(rutas.listaVertices[i][0]+k,rutas.listaVertices[i][1]-1), "Destination"] in listRoad:
                                conexionDes.append((rutas.listaVertices[i],(rutas.listaVertices[i][0]+k,rutas.listaVertices[i][1]-1),k+1))
                                rutas.agregarArista(rutas.listaVertices[i],(rutas.listaVertices[i][0]+k,rutas.listaVertices[i][1]-1),k+1)
                                
                            elif [(rutas.listaVertices[i][0]+k,rutas.listaVertices[i][1]+2),"Destination"] in listRoad and [(rutas.listaVertices[i][0]+k,rutas.listaVertices[i][1]+1),"Right"] in listRoad:
                                conexionDes.append((rutas.listaVertices[i],(rutas.listaVertices[i][0]+k,rutas.listaVertices[i][1]+2),k+2))
                                rutas.agregarArista(rutas.listaVertices[i],(rutas.listaVertices[i][0]+k,rutas.listaVertices[i][1]+2),k+2)
                                
                            elif [(rutas.listaVertices[i][0]+k,rutas.listaVertices[i][1]-2), "Destination"] in listRoad and [(rutas.listaVertices[i][0]+k,rutas.listaVertices[i][1]-1), "Right"] in listRoad:
                                conexionDes.append((rutas.listaVertices[i],(rutas.listaVertices[i][0]+k,rutas.listaVertices[i][1]-2),k+2))
                                rutas.agregarArista(rutas.listaVertices[i],(rutas.listaVertices[i][0]+k,rutas.listaVertices[i][1]-2),k+2)
                              
            if listInt[i] == "DownRight":
                for j in range(len(listaX)):
                    if rutas.listaVertices[i][0] == listaX[j]:
                        if rutas.listaVertices[i][1]-listaY[j] > 0:
                            subY.append(rutas.listaVertices[i][1]-listaY[j])
                            posicionVer.append((listaX[j],listaY[j]))       
                    elif rutas.listaVertices[i][1] == listaY[j]:
                        if listaX[j]-rutas.listaVertices[i][0] > 0:
                            subX.append(listaX[j]-rutas.listaVertices[i][0])
                            posicionHor.append((listaX[j],listaY[j]))
                            
                if len(subY)>0:
                    if min(subY)>1:
                        for k in range(min(subY)):
                            if [(rutas.listaVertices[i][0]+1,rutas.listaVertices[i][1]-k), "Destination"] in listRoad:
                                conexionDes.append((rutas.listaVertices[i],(rutas.listaVertices[i][0]+1,rutas.listaVertices[i][1]+k),k+1))
                                rutas.agregarArista(rutas.listaVertices[i],(rutas.listaVertices[i][0]+1,rutas.listaVertices[i][1]+k),k+1)
                                
                            elif [(rutas.listaVertices[i][0]-1,rutas.listaVertices[i][1]-k), "Destination"] in listRoad:
                                conexionDes.append((rutas.listaVertices[i],(rutas.listaVertices[i][0]-1,rutas.listaVertices[i][1]-k),k+1))
                                rutas.agregarArista(rutas.listaVertices[i],(rutas.listaVertices[i][0]-1,rutas.listaVertices[i][1]-k),k+1)
                                
                            elif [(rutas.listaVertices[i][0]+2,rutas.listaVertices[i][1]-k), "Destination"] in listRoad and [(rutas.listaVertices[i][0]+1,rutas.listaVertices[i][1]-k), "Down"] in listRoad:
                                conexionDes.append((rutas.listaVertices[i],(rutas.listaVertices[i][0]+2,rutas.listaVertices[i][1]+k),k+2))
                                rutas.agregarArista(rutas.listaVertices[i],(rutas.listaVertices[i][0]+2,rutas.listaVertices[i][1]+k),k+2)
                                
                            elif [(rutas.listaVertices[i][0]-2,rutas.listaVertices[i][1]-k), "Destination"] in listRoad and [(rutas.listaVertices[i][0]-1,rutas.listaVertices[i][1]-k), "Down"] in listRoad:
                                conexionDes.append((rutas.listaVertices[i],(rutas.listaVertices[i][0]-2,rutas.listaVertices[i][1]-k),k+2))
                                rutas.agregarArista(rutas.listaVertices[i],(rutas.listaVertices[i][0]-2,rutas.listaVertices[i][1]-k),k+2)
                
                if len(subX)>0:
                    if min(subX)>1:
                        for k in range(min(subX)):
                            if [(rutas.listaVertices[i][0]+k,rutas.listaVertices[i][1]+1),"Destination"] in listRoad:
                                conexionDes.append((rutas.listaVertices[i],(rutas.listaVertices[i][0]+k,rutas.listaVertices[i][1]+1),k+1))
                                rutas.agregarArista(rutas.listaVertices[i],(rutas.listaVertices[i][0]+k,rutas.listaVertices[i][1]+1),k+1)
                                
                            elif [(rutas.listaVertices[i][0]+k,rutas.listaVertices[i][1]-1), "Destination"] in listRoad:
                                conexionDes.append((rutas.listaVertices[i],(rutas.listaVertices[i][0]+k,rutas.listaVertices[i][1]-1),k+1))
                                rutas.agregarArista(rutas.listaVertices[i],(rutas.listaVertices[i][0]+k,rutas.listaVertices[i][1]-1),k+1)
                                
                            elif [(rutas.listaVertices[i][0]+k,rutas.listaVertices[i][1]+2),"Destination"] in listRoad and [(rutas.listaVertices[i][0]+k,rutas.listaVertices[i][1]+1),"Right"] in listRoad:
                                conexionDes.append((rutas.listaVertices[i],(rutas.listaVertices[i][0]+k,rutas.listaVertices[i][1]+2),k+2))
                                rutas.agregarArista(rutas.listaVertices[i],(rutas.listaVertices[i][0]+k,rutas.listaVertices[i][1]+2),k+2)
                                
                            elif [(rutas.listaVertices[i][0]+k,rutas.listaVertices[i][1]-2), "Destination"] in listRoad and [(rutas.listaVertices[i][0]+k,rutas.listaVertices[i][1]-1), "Right"] in listRoad:
                                conexionDes.append((rutas.listaVertices[i],(rutas.listaVertices[i][0]+k,rutas.listaVertices[i][1]-2),k+2))
                                rutas.agregarArista(rutas.listaVertices[i],(rutas.listaVertices[i][0]+k,rutas.listaVertices[i][1]-2),k+2)
            
            
            if listInt[i] == "DownLeft":
                for j in range(len(listaX)):
                    if rutas.listaVertices[i][0] == listaX[j]:
                        if rutas.listaVertices[i][1]-listaY[j] > 0:
                            subY.append(rutas.listaVertices[i][1]-listaY[j])
                            posicionVer.append((listaX[j],listaY[j]))
                                     
                    elif rutas.listaVertices[i][1] == listaY[j]:
                        if rutas.listaVertices[i][0]-listaX[j] > 0:
                            subX.append(rutas.listaVertices[i][0]-listaX[j])
                            posicionHor.append((listaX[j],listaY[j]))
                            
                if len(subY)>0:
                    if min(subY)>1:
                        for k in range(min(subY)):
                            if [(rutas.listaVertices[i][0]+1,rutas.listaVertices[i][1]-k), "Destination"] in listRoad:
                                conexionDes.append((rutas.listaVertices[i],(rutas.listaVertices[i][0]+1,rutas.listaVertices[i][1]+k),k+1))
                                rutas.agregarArista(rutas.listaVertices[i],(rutas.listaVertices[i][0]+1,rutas.listaVertices[i][1]+k),k+1)
                                
                            elif [(rutas.listaVertices[i][0]-1,rutas.listaVertices[i][1]-k), "Destination"] in listRoad:
                                conexionDes.append((rutas.listaVertices[i],(rutas.listaVertices[i][0]-1,rutas.listaVertices[i][1]-k),k+1))
                                rutas.agregarArista(rutas.listaVertices[i],(rutas.listaVertices[i][0]-1,rutas.listaVertices[i][1]-k),k+1)
                                
                            elif [(rutas.listaVertices[i][0]+2,rutas.listaVertices[i][1]-k), "Destination"] in listRoad and [(rutas.listaVertices[i][0]+1,rutas.listaVertices[i][1]-k), "Down"] in listRoad:
                                conexionDes.append((rutas.listaVertices[i],(rutas.listaVertices[i][0]+2,rutas.listaVertices[i][1]+k),k+2))
                                rutas.agregarArista(rutas.listaVertices[i],(rutas.listaVertices[i][0]+2,rutas.listaVertices[i][1]+k),k+2)
                                
                            elif [(rutas.listaVertices[i][0]-2,rutas.listaVertices[i][1]-k), "Destination"] in listRoad and [(rutas.listaVertices[i][0]-1,rutas.listaVertices[i][1]-k), "Down"] in listRoad:
                                conexionDes.append((rutas.listaVertices[i],(rutas.listaVertices[i][0]-2,rutas.listaVertices[i][1]-k),k+2))
                                rutas.agregarArista(rutas.listaVertices[i],(rutas.listaVertices[i][0]-2,rutas.listaVertices[i][1]-k),k+2)
                
                if len(subX)>0:
                    if min(subX)>1:
                        for k in range(min(subX)):
                            if [(rutas.listaVertices[i][0]-k,rutas.listaVertices[i][1]+1),"Destination"] in listRoad:
                                conexionDes.append((rutas.listaVertices[i],(rutas.listaVertices[i][0]-k,rutas.listaVertices[i][1]+1),k+1))
                                rutas.agregarArista(rutas.listaVertices[i],(rutas.listaVertices[i][0]-k,rutas.listaVertices[i][1]+1),k+1)
                                
                            elif [(rutas.listaVertices[i][0]-k,rutas.listaVertices[i][1]-1), "Destination"] in listRoad:
                                conexionDes.append((rutas.listaVertices[i],(rutas.listaVertices[i][0]-k,rutas.listaVertices[i][1]-1),k+1))
                                rutas.agregarArista(rutas.listaVertices[i],(rutas.listaVertices[i][0]-k,rutas.listaVertices[i][1]-1),k+1)
                                
                            elif [(rutas.listaVertices[i][0]-k,rutas.listaVertices[i][1]+2),"Destination"] in listRoad and [(rutas.listaVertices[i][0]-k,rutas.listaVertices[i][1]+1),"Left"] in listRoad:
                                conexionDes.append((rutas.listaVertices[i],(rutas.listaVertices[i][0]-k,rutas.listaVertices[i][1]+2),k+2))
                                rutas.agregarArista(rutas.listaVertices[i],(rutas.listaVertices[i][0]-k,rutas.listaVertices[i][1]+2),k+2)
                                
                            elif [(rutas.listaVertices[i][0]-k,rutas.listaVertices[i][1]-2), "Destination"] in listRoad and [(rutas.listaVertices[i][0]-k,rutas.listaVertices[i][1]-1), "Left"] in listRoad:
                                conexionDes.append((rutas.listaVertices[i],(rutas.listaVertices[i][0]-k,rutas.listaVertices[i][1]-2),k+2))
                                rutas.agregarArista(rutas.listaVertices[i],(rutas.listaVertices[i][0]-k,rutas.listaVertices[i][1]-2),k+2)
                                
                
            if len(subY)>0:
                conexionVer.append((rutas.listaVertices[i],posicionVer[subY.index(min(subY))],min(subY)))
                rutas.agregarArista(rutas.listaVertices[i],posicionVer[subY.index(min(subY))],min(subY))
                posicionVer=[]
                subY=[]
            if len(subX)>0:
                conexionHor.append((rutas.listaVertices[i],posicionHor[subX.index(min(subX))],min(subX)))
                rutas.agregarArista(rutas.listaVertices[i],posicionHor[subX.index(min(subX))],min(subX))
                posicionHor=[]
                subX=[]

        print(conexionVer)
        print("---------------------------------------")
        print(conexionHor)
        print("---------------------------------------")
        print(conexionDes)
        print(len(conexionDes))
                    
        #rutas.agregarArista(rutas.listaVertices[misVertices],listRoad[g][0],peso)
        #print(listRoad)
        #print(rutas.listaVertices)
        print("\n\nLa ruta mas rapida por Dijkstra junto con su costo es:")
        rutas.dijkstra((0,0))
        print(rutas.camino((0,0),(5,4)))
        print("\nLos valores finales de la grafica son los siguientes:")
        rutas.imprimirGrafica()           
        #print(rutas.imprimir_matriz(rutas.matriz))    
        self.num_agents = N
        listaWaze=[]
        for i in range(N) :
            pos = (0,0)
            pos_1 = (0,23)
            pos_5 = (1,23)
            pos_2 = (23,0)
            pos_6 = (23,1)
            pos_3 = (23,23)
            pos_7 = (23,24)
            position = [pos, pos_1, pos_2, pos_3, pos_5, pos_6, pos_7]
            destination = random.choice(self.destination_pos)
            if pos not in self.occupied:
                car = Car(self.next_id(),self, destination, rutas)
                self.schedule.add(car)
                self.grid.place_agent(car,random.choice(position))
                self.occupied.append((position))
                print(str("id carro ") + str(car))
                print(str("destino") + str(destination) + str(car))
                #break
        self.running = True

    def step(self):
        '''Advance the model by one step.'''
        if self.schedule.steps % 10 == 0:
            for agent in self.traffic_lights:
                agent.state = not agent.state
        self.schedule.step()