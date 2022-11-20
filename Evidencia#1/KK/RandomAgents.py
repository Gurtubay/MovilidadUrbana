# -----
# Descripción Breve:
#   Esta es una simulación de multiagentes con el fin de estudiar las estadísticas 
#   de un robot Stevedor organizando cajas. 
# -----
# Autores:
#   Sebastián Burgos Alanís A01746459 
#   Josue Yorke
#   José Guturbay
#   Fabio
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

class Stevedor(mesa.Agent):
    # Clase para crear el Agente, definir su acción y su movimiento. 
    # Constructor del agente de Stevedor y sus atributos.
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.carring = False
        self.piles_plus = 0
        self.piles = 0
        self.box_limit = [] #queria hacer una lista con las posiciones de los stacks para que no tomaran cajs de ahí

    # Si la celda tiene Box, la cargará. 
    def step(self):
        if self.carring == True:
            self.move_1_1()
            print("step" + str(self.piles))
        else:
            self.move()
            position = self.model.grid.get_cell_list_contents([self.pos])
            box = [obj for obj in position if isinstance(obj, Box)]
            if len(box) > 0:
                self.carring = True
                self.box_carried = self.random.choice(box)
                if self.piles == 5: #numero de cajas por stacks
                    self.piles = 0 #numero de cajas
                    self.piles_plus += 1 #stacks
            

    #teniendo la Box, se moverá a la posición indicada para apliar las cajas. 
    def move_1_1(self):
        x,y = self.pos
        self.piles
        self.piles_plus
        if x > self.piles_plus+1:
            self.model.grid.move_agent(self,(x-1,y))
            self.model.grid.move_agent(self.box_carried,(x-1,y))
        elif x == 0+self.piles_plus:
            self.model.grid.move_agent(self,(x+1,y))
            self.model.grid.move_agent(self.box_carried,(x+1,y))
        elif y > 1:
            self.model.grid.move_agent(self,(x,y-1))
            self.model.grid.move_agent(self.box_carried,(x,y-1))
        elif y == 0:
            self.model.grid.move_agent(self,(x,y+1))
            self.model.grid.move_agent(self.box_carried,(x,y+1))
        elif x == self.piles_plus+1 and y == 1:
            self.carring = False
            self.piles += 1
            
            
    # Función para mover al agente a una posición aleatoria disponible.
    def move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, True, True)
        chosen_step = self.random.choice(possible_steps)
        position = self.model.grid.get_cell_list_contents([chosen_step])
        stevedor = [obj for obj in position if isinstance(obj, Stevedor)]
        if len(stevedor) < 1:
            self.model.grid.move_agent(self, chosen_step)
            

class Box(mesa.Agent):
    # Constructor para la creación de la Box. 
    def __init__(self,unique_id,model):
        super().__init__(unique_id, model)

#-------------#
#--- MODEL ---#
#-------------#

class CarringModel(Model):
    # Clase para definir el Modelo, asiganción de variables, creación de 1 o más Agentes. 
    # Constructor del Modelo con las variables requeridas
    def __init__(self,width,height,X,p,e):
        super().__init__()
        self.width = width
        self.height = height
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)
        self.currentsteps = 0
        self.maxsteps = e
        d = (p*(width*height))/100

        # Creación de los Agentes
        for i in range(X):
            carr = Stevedor(self.next_id(),self)
            self.schedule.add(carr)
            self.grid.place_agent(carr,(1,1))
            
        # Colocación aleatoria de la Box. 
        for i in range(round(d)):
            boxes = Box(self.next_id(),self)
            self.schedule.add(boxes)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(boxes,(x,y))
    
    def step(self):
        self.schedule.step()


#--------------#
#--- SERVER ---#
#--------------#

"""
def cleaning_port(agent):
    # Función para crear el servidor, el Canvas, asignar el puerto de servidor,
    #   definir los colores y figuras de los agentes así como la asiganción de los valores para 
    #   crear Numero de Agentes, Espacio de habitación, Porcentaje de Boxes y tiempo de ejecución. 
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
server = ModularServer(CarringModel,[grid],"carringModel",{"width":10,"height":10,"x":1,"p":25,"e":100})

chart_element = mesa.visualization.ChartModule(
    [
        {"Label":"Box","Color":"#AA0000"}
    ])

# Puerto de salida de transmisión. 
server.port = 851 

# Lanzamiento del servidor. 
server.launch()
"""