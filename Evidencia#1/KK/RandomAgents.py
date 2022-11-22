# -----
# Descripción Breve:
#   Esta es una simulación de multiagentes con el fin de estudiar las estadísticas 
#   de un robot Stevedor organizando cajas. 
# -----
# Autores:
#   Sebastián Burgos Alanís A01746459 
#   Josué Bernardo Villegas Nuño A01751694
#   José Guturbay Moreno A01373750
#   Favio Mariano Dileva Charles A01745465
# -----
# Fecha de creación:
#   17/11/22
# Fecha de modificación:
#   19/10/22
# -----

import mesa
from mesa import Model
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid

#-------------#
#--- AGENT ---#
#-------------#
piles=0
puntoX=0
box_limit=[]
"""
Clase del agente "Stevedor" el robot que se encargara de transportar y apilar las cajas
"""
class Stevedor(mesa.Agent):
    # Clase para crear el Agente, definir su acción y su movimiento. 
    # Constructor del agente de Stevedor y sus atributos.
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.carring = False #Variable con el estado actual del robot si esta cargando con una caja o no
        #self.files_plus = 0 #Variable con la posicion en x de donde seran apiladas las cajas
        #self.piles = 0 #Variable que cuenta las cajas en una misma pila
        self.stepsCount = 0 #Cuenta los pasos de cada agente
        self.boxCount = 0 #Cuenta las cajas procesadas por cada agente
        self.stack_actual = (0,1) #Coordenadas de la posicion de la primera pila de cajas
        #box_limit = [] #queria hacer una lista con las posiciones de los stacks para que no tomaran cajs de ahí
        
        
 
    """
    Funcion que le permite al robot moverse aleatoreamente hasta encontrar una caja, entonces el robot cargara la caja y se movera a la posicion de apilado
    """
    def step(self):
        global puntoX
        self.stepsCount +=1
        if self.carring == True:
            self.move_1_1()
            print("hermana del Jos" +str([self.pos]))
        else:
            self.move()
            if self.pos not in box_limit:
                position = self.model.grid.get_cell_list_contents([self.pos])
                box = [obj for obj in position if isinstance(obj, Box)]
                if len(box) > 0:
                    self.carring = True
                    self.box_carried = self.random.choice(box)
                    #if self.piles == 5: #numero de cajas por stacks
    """
    Funcion que cuenta la cantidad de cajas en una pila y determina cuando hay que hacer una nueva pila y en donde estara esta nueva pila, ademas de bloquear las cajas ya apiladas
    """
    def stack(self):
        global piles
        global puntoX
        if piles==0:
            box_limit.append((puntoX,1))
        piles +=1
        print(piles)
        self.carring = False
        print(self.boxCount)
        self.boxCount +=1
        print(self.boxCount)
        if piles == 5:
            piles=0 #numero de cajas
            print(puntoX)
            puntoX += 1 #stacks
            print(puntoX)

    """
    Funcion para que el robot se mueva a la poisicon de apilado actual
    """
    def move_1_1(self):
        x,y = self.pos
        #self.piles
        puntoX

        if x != puntoX:
            direccion = -1 if puntoX - x < 0 else 1 #direccion
            self.model.grid.move_agent(self,(x + direccion,y))
            self.model.grid.move_agent(self.box_carried,(x + direccion,y))
            return
        
        elif y != 1:
            direccion = -1 if 1 - y < 0 else 1 #direccion
            self.model.grid.move_agent(self,(x,y + direccion))
            self.model.grid.move_agent(self.box_carried,(x,y + direccion))
            return

        else:
            self.stack()
            
    """
    Funcion para que el robot se mueva aleatoreamente
    """
    
    def move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, True, True)
        chosen_step = self.random.choice(possible_steps)
        position = self.model.grid.get_cell_list_contents([chosen_step])
        stevedor = [obj for obj in position if isinstance(obj, Stevedor)]
        if len(stevedor) < 1:
            self.model.grid.move_agent(self, chosen_step)
            
"""
Clase del agente caja
"""
class Box(mesa.Agent):
    # Constructor para la creación de la Box. 
    def __init__(self,unique_id,model):
        super().__init__(unique_id, model)

#-------------#
#--- MODEL ---#
#-------------#

"""
Clase para definir el Modelo, asiganción de variables, creación de 1 o más Agentes. 
Constructor del Modelo con las variables requeridas
"""
class CarringModel(Model):
    def __init__(self,width,height,X,p,e):
        super().__init__()
        self.width = width
        self.height = height
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)
        self.currentsteps = 0
        self.maxsteps = e
        self.occupied=[]
        d = (p*(width*height))/100

        # Creación de los Agentes
        for i in range(X):
            while True:
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                pos=(x,y)
                if pos not in self.occupied:
                    carr = Stevedor(self.next_id(),self)
                    self.schedule.add(carr)
                    self.grid.place_agent(carr,(pos))
                    self.occupied.append((pos))
                    break
            
        # Colocación aleatoria de la Box. 
        for i in range(round(d)):
            while True:
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                pos=(x,y)
                if pos not in self.occupied:
                    boxes = Box(self.next_id(),self)
                    self.schedule.add(boxes)
                    self.grid.place_agent(boxes,(pos))
                    self.occupied.append((pos))
                    break
    
    def step(self):
        self.schedule.step()
"""

#--------------#
#--- SERVER ---#
#--------------#


Función para crear el servidor, el Canvas, asignar el puerto de servidor,
definir los colores y figuras de los agentes así como la asiganción de los valores para 
crear Numero de Agentes, Espacio de habitación, Porcentaje de Boxes y tiempo de ejecución. 

def cleaning_port(agent):

    portrayal = {"Shape":"circle","Filled":"true", "r":0.5}
    square = {"Shape":"square", "Filled":"true", }
    # Diseño de los Agentes
    if type(agent) is Stevedor:
        portrayal["Color"] = "green"
        portrayal["Layer"] = 1
    
    # Diseño de la Caja. 
    else:
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.2

    return portrayal

# Diseño del Canvas y definición de valores. 
grid = CanvasGrid(cleaning_port, 10, 10, 500, 500)
server = ModularServer(CarringModel,[grid],"carringModel",{"width":10,"height":10,"X":1,"p":25,"e":100})

chart_element = mesa.visualization.ChartModule(
    [
        {"Label":"Box","Color":"#AA0000"}
    ])

# Puerto de salida de transmisión. 
server.port = 851 

# Lanzamiento del servidor. 
server.launch()
"""