from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from agent import *
import json
import math

class Grafo:
    def __init__(self):
        self.vertices = []
        self.matriz = [[None]*0 for i in range(0)]

    def imprimir_matriz(self, m):
        cadena = ""

        for c in range(len(m)):
            cadena += "\t" + str(self.vertices[c])

        cadena += "\n " + ("         -" * len(m))

        for f in range(len(m)):
            cadena += "\n" + str(self.vertices[f]) + " |"
            for c in range(len(m)):
                if f == c and (m[f][c] is None or m[f][c] == 0):
                        cadena += "\t" + "\\"
                else:
                    if f == c and (m[f][c] is None or m[f][c] == 0):
                        cadena += "\t" + "\\"
                    else:
                        if m[f][c] is None or math.isinf(m[f][c]):
                            cadena += "\t" + "X"
                        else:
                            cadena += "\t" + str(m[f][c])

        cadena += "\n"
        print(cadena)

    @staticmethod
    def contenido_en(lista, k):
        if lista.count(k) == 0:
            return False
        return True

    def esta_en_vertices(self, v):
        if self.vertices.count(v) == 0:
            return False
        return True

    def agregar_vertices(self, v):
        if self.esta_en_vertices(v):
            return False
        # Si no esta contenido.
        self.vertices.append(v)

        # Redimensiono la matriz de adyacencia.
        # Para preparalarla para agregar más Aristas.
        filas = columnas = len(self.matriz)
        matriz_aux = [[None] * (filas+1) for i in range(columnas+1)]

        # Recorro la matriz y copio su contenido dentro de la matriz más grande.
        for f in range(filas):
            for c in range(columnas):
                matriz_aux[f][c] = self.matriz[f][c]

        # Igualo la matriz a la matriz más grande.
        self.matriz = matriz_aux
        return True

    def agregar_arista(self, inicio, fin, valor, dirijida):
        if not(self.esta_en_vertices(inicio)) or not(self.esta_en_vertices(fin)):
            return False
        # Si estan contenidos en la lista de vertices.
        self.matriz[self.vertices.index(inicio)][self.vertices.index(fin)] = valor

        # Si la arista entrante no es dirijida.
        # Instancio una Arista en sentido contrario de Fin a Inicio.
        if not dirijida:
            self.matriz[self.vertices.index(fin)][self.vertices.index(inicio)] = valor
        return True
   
class RandomModel(Model):
    """ 
    Creates a new model with random agents.
    Args:
        N: Number of agents in the simulation
    """
    def __init__(self, N):
        
        #rutas = Grafo(self.next_id,self)
        rutas=Grafo()
        listaRoad=[]
        listaIntersecciones=[]
        super().__init__()
        dataDictionary = json.load(open("mapDictionary.json"))

        self.destination_pos= []

        self.traffic_lights = []
        self.occupied=[]
        with open('2022_base.txt') as baseFile:
            lines = baseFile.readlines()
            self.width = len(lines[0])-1
            self.height = len(lines)

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
                        listaRoad.append([agent.pos, agent.direction])
                        if col in ["$","&","%","*"]:
                            rutas.agregar_vertices((c, self.height - r - 1))
                            listaIntersecciones.append(dataDictionary[col])
                        
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
                        rutas.agregar_vertices((c, self.height - r - 1))
                        listaIntersecciones.append("Destination")
                    
        ##rutas.imprimir_matriz(rutas.matriz)
        peso=1
        misVertices=0
        
        for i in range(len(rutas.vertices)):
            for g in range(len(listaRoad)):
                if listaRoad[g][0][0]==rutas.vertices[misVertices][0]+1 or listaRoad[g][0][0]==rutas.vertices[misVertices][0]-1 or listaRoad[g][0][1]==rutas.vertices[misVertices][1]+1 or listaRoad[g][0][1]==rutas.vertices[misVertices][1]-1:
                    if listaIntersecciones[misVertices]=="UpLeft":
                        if listaRoad[g][1]<"Up":
                            while True:
                                if [(listaRoad[g][0][0],listaRoad[g][0][1]+peso),"Up"] in listaRoad:
                                    peso+=1
                                    if (listaRoad[g][0][0]+1,listaRoad[g][0][1]+peso) in self.destination_pos:
                                        rutas.agregar_arista(rutas.vertices[misVertices],(listaRoad[g][0][0]+1,listaRoad[g][0][1]),peso+1,True)
                                        
                                    elif (listaRoad[g][0][0]-1,listaRoad[g][0][1]+peso) in self.destination_pos:
                                        rutas.agregar_arista(rutas.vertices[misVertices],(listaRoad[g][0][0]-1,listaRoad[g][0][1]),peso+1,True)
                                        
                                    elif (listaRoad[g][0][0]+2,listaRoad[g][0][1]+peso) in self.destination_pos and [(listaRoad[g][0][0]+1,listaRoad[g][0][1]+peso),"Up"] in listaRoad:
                                        rutas.agregar_arista(rutas.vertices[misVertices],(listaRoad[g][0][0]+2,listaRoad[g][0][1]),peso+2,True)
                                        
                                    elif (listaRoad[g][0][0]-2,listaRoad[g][0][1]+peso) in self.destination_pos and [(listaRoad[g][0][0]-1,listaRoad[g][0][1]+peso),"Up"] in listaRoad:
                                        rutas.agregar_arista(rutas.vertices[misVertices],(listaRoad[g][0][0]-2,listaRoad[g][0][1]),peso+2,True)
                                else:
                                    break
                            rutas.agregar_arista(rutas.vertices[misVertices],listaRoad[g][0],peso,True)
                            peso=1
                        elif listaRoad[g][1]<"Left":
                            while True:
                                if [(listaRoad[g][0][0]-peso,listaRoad[g][0][1]),"Left"] in listaRoad:
                                    peso+=1
                                    if (listaRoad[g][0][0],listaRoad[g][0][1]+1) in self.destination_pos:
                                        rutas.agregar_arista(rutas.vertices[misVertices],(listaRoad[g][0][0],listaRoad[g][1]+1),peso+1,True)
                                        
                                    elif (listaRoad[g][0][0],listaRoad[g][0][1]-1) in self.destination_pos:
                                        rutas.agregar_arista(rutas.vertices[misVertices],(listaRoad[g][0][0],listaRoad[g][1]-1),peso+1,True)
                                        
                                    elif (listaRoad[g][0][0],listaRoad[g][0][1]+2) in self.destination_pos and [(listaRoad[g][0][0]-peso,listaRoad[g][0][1]+1),"Left"] in listaRoad:
                                        rutas.agregar_arista(rutas.vertices[misVertices],(listaRoad[g][0][0],listaRoad[g][1]+2),peso+2,True)
                                        
                                    elif (listaRoad[g][0][0],listaRoad[g][0][1]-2) in self.destination_pos and [(listaRoad[g][0][0]-peso,listaRoad[g][0][1]-1),"Left"] in listaRoad:
                                        rutas.agregar_arista(rutas.vertices[misVertices],(listaRoad[g][0][0],listaRoad[g][1]-2),peso+2,True)
                                else:
                                    break
                            rutas.agregar_arista(rutas.vertices[misVertices],listaRoad[g][0],peso,True)
                            peso=1
                        elif listaRoad[g][1]<"UpLeft":
                            rutas.agregar_arista(rutas.vertices[misVertices],listaRoad[g][0],peso,True)
                    
                    elif listaIntersecciones[misVertices]=="UpRight":
                        if listaRoad[g][1]<"Up":
                            while True:
                                if [(listaRoad[g][0][0],listaRoad[g][0][1]+peso),"Up"] in listaRoad:
                                    peso+=1
                                    if (listaRoad[g][0][0]+1,listaRoad[g][0][1]+peso) in self.destination_pos:
                                        rutas.agregar_arista(rutas.vertices[misVertices],(listaRoad[g][0][0]+1,listaRoad[g][0][1]),peso+1,True)
                                        
                                    elif (listaRoad[g][0][0]-1,listaRoad[g][0][1]+peso) in self.destination_pos:
                                        rutas.agregar_arista(rutas.vertices[misVertices],(listaRoad[g][0][0]-1,listaRoad[g][0][1]),peso+1,True)
                                        
                                    elif (listaRoad[g][0][0]+2,listaRoad[g][0][1]+peso) in self.destination_pos and [(listaRoad[g][0][0]+1,listaRoad[g][0][1]+peso),"Up"] in listaRoad:
                                        rutas.agregar_arista(rutas.vertices[misVertices],(listaRoad[g][0][0]+2,listaRoad[g][0][1]),peso+2,True)
                                        
                                    elif (listaRoad[g][0][0]-2,listaRoad[g][0][1]+peso) in self.destination_pos and [(listaRoad[g][0][0]-1,listaRoad[g][0][1]+peso),"Up"] in listaRoad:
                                        rutas.agregar_arista(rutas.vertices[misVertices],(listaRoad[g][0][0]-2,listaRoad[g][0][1]),peso+2,True)
                                else:
                                    break
                            rutas.agregar_arista(rutas.vertices[misVertices],listaRoad[g][0],peso,True)
                            peso=1
                            
                        elif listaRoad[g][1]<"Right":
                            while True:
                                if [(listaRoad[g][0][0]-peso,listaRoad[g][0][1]),"Right"] in listaRoad:
                                    peso+=1
                                    if (listaRoad[g][0][0],listaRoad[g][0][1]+1) in self.destination_pos:
                                        rutas.agregar_arista(rutas.vertices[misVertices],(listaRoad[g][0][0],listaRoad[g][1]+1),peso+1,True)
                                        
                                    elif (listaRoad[g][0][0],listaRoad[g][0][1]-1) in self.destination_pos:
                                        rutas.agregar_arista(rutas.vertices[misVertices],(listaRoad[g][0][0],listaRoad[g][1]-1),peso+1,True)
                                        
                                    elif (listaRoad[g][0][0],listaRoad[g][0][1]+2) in self.destination_pos and [(listaRoad[g][0][0]-peso,listaRoad[g][0][1]+1),"Left"] in listaRoad:
                                        rutas.agregar_arista(rutas.vertices[misVertices],(listaRoad[g][0][0],listaRoad[g][1]+2),peso+2,True)
                                        
                                    elif (listaRoad[g][0][0],listaRoad[g][0][1]-2) in self.destination_pos and [(listaRoad[g][0][0]-peso,listaRoad[g][0][1]-1),"Left"] in listaRoad:
                                        rutas.agregar_arista(rutas.vertices[misVertices],(listaRoad[g][0][0],listaRoad[g][1]-2),peso+2,True)
                                else:
                                    break
                            rutas.agregar_arista(rutas.vertices[misVertices],listaRoad[g][0],peso,True)
                            peso=1
                            
                        elif listaRoad[g][1]<"UpRight":
                            rutas.agregar_arista(rutas.vertices[misVertices],listaRoad[g][0],peso,True)
                            
                    elif listaIntersecciones[misVertices]=="DownLeft":
                        if listaRoad[g][1]<"Down":
                            while True:
                                if [(listaRoad[g][0][0],listaRoad[g][0][1]+peso),"Down"] in listaRoad:
                                    peso+=1
                                    if (listaRoad[g][0][0]+1,listaRoad[g][0][1]+peso) in self.destination_pos:
                                        rutas.agregar_arista(rutas.vertices[misVertices],(listaRoad[g][0][0]+1,listaRoad[g][0][1]),peso+1,True)
                                        
                                    elif (listaRoad[g][0][0]-1,listaRoad[g][0][1]+peso) in self.destination_pos:
                                        rutas.agregar_arista(rutas.vertices[misVertices],(listaRoad[g][0][0]-1,listaRoad[g][0][1]),peso+1,True)
                                        
                                    elif (listaRoad[g][0][0]+2,listaRoad[g][0][1]+peso) in self.destination_pos and [(listaRoad[g][0][0]+1,listaRoad[g][0][1]+peso),"Down"] in listaRoad:
                                        rutas.agregar_arista(rutas.vertices[misVertices],(listaRoad[g][0][0]+2,listaRoad[g][0][1]),peso+2,True)
                                        
                                    elif (listaRoad[g][0][0]-2,listaRoad[g][0][1]+peso) in self.destination_pos and [(listaRoad[g][0][0]-1,listaRoad[g][0][1]+peso),"Down"] in listaRoad:
                                        rutas.agregar_arista(rutas.vertices[misVertices],(listaRoad[g][0][0]-2,listaRoad[g][0][1]),peso+2,True)
                                else:
                                    break
                            rutas.agregar_arista(rutas.vertices[misVertices],listaRoad[g][0],peso,True)
                            peso =1
                            
                        elif listaRoad[g][1]<"Left":
                            while True:
                                if [(listaRoad[g][0][0]-peso,listaRoad[g][0][1]),"Left"] in listaRoad:
                                    peso+=1
                                    if (listaRoad[g][0][0],listaRoad[g][0][1]+1) in self.destination_pos:
                                        rutas.agregar_arista(rutas.vertices[misVertices],(listaRoad[g][0][0],listaRoad[g][1]+1),peso+1,True)
                                        
                                    elif (listaRoad[g][0][0],listaRoad[g][0][1]-1) in self.destination_pos:
                                        rutas.agregar_arista(rutas.vertices[misVertices],(listaRoad[g][0][0],listaRoad[g][1]-1),peso+1,True)
                                        
                                    elif (listaRoad[g][0][0],listaRoad[g][0][1]+2) in self.destination_pos and [(listaRoad[g][0][0]-peso,listaRoad[g][0][1]+1),"Left"] in listaRoad:
                                        rutas.agregar_arista(rutas.vertices[misVertices],(listaRoad[g][0][0],listaRoad[g][1]+2),peso+2,True)
                                        
                                    elif (listaRoad[g][0][0],listaRoad[g][0][1]-2) in self.destination_pos and [(listaRoad[g][0][0]-peso,listaRoad[g][0][1]-1),"Left"] in listaRoad:
                                        rutas.agregar_arista(rutas.vertices[misVertices],(listaRoad[g][0][0],listaRoad[g][1]-2),peso+2,True)
                                else:
                                    break
                            rutas.agregar_arista(rutas.vertices[misVertices],listaRoad[g][0],peso,True)
                            peso=1
                            
                        elif listaRoad[g][1]<"DownLeft":
                            rutas.agregar_arista(rutas.vertices[misVertices],listaRoad[g][0],peso,True)
                            
                    elif listaIntersecciones[misVertices]=="DownRight":
                        if listaRoad[g][1]<"Down":
                            while True:
                                if [(listaRoad[g][0][0],listaRoad[g][0][1]+peso),"Down"] in listaRoad:
                                    peso+=1
                                    if [(listaRoad[g][0][0]+1,listaRoad[g][0][1]+peso)] in self.destination_pos:
                                        rutas.agregar_arista(rutas.vertices[misVertices],(listaRoad[g][0][0]+1,listaRoad[g][0][1]),peso+1,True)
                                        
                                    elif [(listaRoad[g][0][0]-1,listaRoad[g][0][1]+peso)] in self.destination_pos:
                                        rutas.agregar_arista(rutas.vertices[misVertices],(listaRoad[g][0][0]-1,listaRoad[g][0][1]),peso+1,True)
                                        
                                    elif [(listaRoad[g][0][0]+2,listaRoad[g][0][1]+peso)] in self.destination_pos and [(listaRoad[g][0][0]+1,listaRoad[g][0][1]+peso),"Up"] in listaRoad:
                                        rutas.agregar_arista(rutas.vertices[misVertices],(listaRoad[g][0][0]+2,listaRoad[g][0][1]),peso+2,True)
                                        
                                    elif [(listaRoad[g][0][0]-2,listaRoad[g][0][1]+peso)] in self.destination_pos and [(listaRoad[g][0][0]-1,listaRoad[g][0][1]+peso),"Up"] in listaRoad:
                                        rutas.agregar_arista(rutas.vertices[misVertices],(listaRoad[g][0][0]-2,listaRoad[g][0][1]),peso+2,True)
                                else:
                                    break
                            rutas.agregar_arista(rutas.vertices[misVertices],listaRoad[g][0],peso,True)
                            peso =1
                            
                        elif listaRoad[g][1]<"Right":
                            while True:
                                if [(listaRoad[g][0][0]-peso,listaRoad[g][0][1]),"Right"] in listaRoad:
                                    peso+=1
                                    if (listaRoad[g][0][0],listaRoad[g][0][1]+1) in self.destination_pos:
                                        rutas.agregar_arista(rutas.vertices[misVertices],(listaRoad[g][0][0],listaRoad[g][1]+1),peso+1,True)
                                        
                                    elif (listaRoad[g][0][0],listaRoad[g][0][1]-1) in self.destination_pos:
                                        rutas.agregar_arista(rutas.vertices[misVertices],(listaRoad[g][0][0],listaRoad[g][1]-1),peso+1,True)
                                        
                                    elif (listaRoad[g][0][0],listaRoad[g][0][1]+2) in self.destination_pos and [(listaRoad[g][0][0]-peso,listaRoad[g][0][1]+1),"Left"] in listaRoad:
                                        rutas.agregar_arista(rutas.vertices[misVertices],(listaRoad[g][0][0],listaRoad[g][1]+2),peso+2,True)
                                        
                                    elif (listaRoad[g][0][0],listaRoad[g][0][1]-2) in self.destination_pos and [(listaRoad[g][0][0]-peso,listaRoad[g][0][1]-1),"Left"] in listaRoad:
                                        rutas.agregar_arista(rutas.vertices[misVertices],(listaRoad[g][0][0],listaRoad[g][1]-2),peso+2,True)
                                else:
                                    break
                            rutas.agregar_arista(rutas.vertices[misVertices],listaRoad[g][0],peso,True)
                            peso=1
                            
                        elif listaRoad[g][1]<"DownRight":
                            rutas.agregar_arista(rutas.vertices[misVertices],listaRoad[g][0],peso,True)
            misVertices +=1
            
        print(rutas.imprimir_matriz(rutas.matriz))    
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
                car = Car(self.next_id(),self, destination,rutas)
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