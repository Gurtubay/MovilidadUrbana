import random
from mesa import Agent

class Car(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID 
        direction: Randomly chosen direction chosen from one of eight directions
    """
    def __init__(self, unique_id, model,des, rutas):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)
        self.destination = des
        self.lastDirection = "Left"
        self.rutas = rutas
        self.Waze = self.rutas.camino(self.pos,self.destination)
        self.reachVertice = 0
        #self.knowledge1=[(pos),obj] <- SENSORES

    def move(self):
        """ 
        Determines if the agent can move in the direction that was chosen
        """ 
        xf,yf = self.destination
        """
        possible_steps = self.model.grid.get_neighborhood(self.pos, True, True)
        #evitar que los coches se encimen unos con los otros
        autos=[obj for obj in possible_steps if isinstance(obj,Car)]
        if autos==0:
            print(f"posible steps{possible_steps}")
            #chosen_step = self.random.choice(possible_steps)
        """
        x0,y0 = self.pos
        position =self.model.grid.get_cell_list_contents([self.pos])
        direccionRoad=[obj for obj in position if isinstance(obj,Road)]
        goOrStop = [obj for obj in position if isinstance(obj,Traffic_Light)]
        print(str(self.unique_id) +"|"+ str(self.Waze))
        print(str(self.unique_id) +"|" +str(self.pos))
        print(str(self.unique_id)+ "|" +str(self.Waze[0][self.reachVertice]))
        if self.Waze[0][self.reachVertice] == self.destination:
            if self.pos[0]==self.destination[0]+1 and self.pos[1]==self.destination[1]+1:
                self.model.grid.move_agent(self,(x0-1,y0-1))
            elif self.pos[0]==self.destination[0]-1 and self.pos[1]==self.destination[1]-1:
                self.model.grid.move_agent(self,(x0+1,y0+1))
            elif self.pos[0]==self.destination[0]-1 and self.pos[1]==self.destination[1]+1:
                self.model.grid.move_agent(self,(x0+1,y0-1))
            elif self.pos[0]==self.destination[0]+1 and self.pos[1]==self.destination[1]-1:
                self.model.grid.move_agent(self,(x0-1,y0+1))
            else:
                print("Ultima recta!!!!!!")
                if (self.pos[0]==self.Waze[0][self.reachVertice][0]-1 or self.pos[0]==self.Waze[0][self.reachVertice][0]+1) and self.pos[1]-self.Waze[0][self.reachVertice][1]<0:
                    self.model.grid.move_agent(self,(x0,y0+1))
                    print("Finalmente hacia arriba")
                    #self.lastDirection="Up"
                elif (self.pos[0]==self.Waze[0][self.reachVertice][0]-1 or self.pos[0]==self.Waze[0][self.reachVertice][0]+1) and self.pos[1]-self.Waze[0][self.reachVertice][1]>0:
                    self.model.grid.move_agent(self,(x0,y0-1))
                    print("Finalmente hacia abajo")
                    #self.lastDirection="Down"
                elif (self.pos[1]==self.Waze[0][self.reachVertice][1]-1 or self.pos[1]==self.Waze[0][self.reachVertice][1]+1) and self.pos[0]-self.Waze[0][self.reachVertice][0]>0:
                    self.model.grid.move_agent(self,(x0-1,y0))
                    print("Finalmente hacia Izq")
                    #self.lastDirection="Left"
                elif (self.pos[1]==self.Waze[0][self.reachVertice][1]-1 or self.pos[1]==self.Waze[0][self.reachVertice][1]+1) and self.pos[0]-self.Waze[0][self.reachVertice][0]<0:
                    self.model.grid.move_agent(self,(x0+1,y0))
                    print("Finalmente hacia Der")
                    #self.lastDirection="Right"
                elif (self.pos[0]==self.Waze[0][self.reachVertice][0]-2 or self.pos[0]==self.Waze[0][self.reachVertice][0]+2) and self.pos[1]-self.Waze[0][self.reachVertice][1]<0:
                    if self.pos[0]-self.Waze[0][self.reachVertice][0]>0:
                        self.model.grid.move_agent(self,(x0-1,y0))
                    else:
                        self.model.grid.move_agent(self,(x0+1,y0))
                    #self.lastDirection="Up"
                elif (self.pos[0]==self.Waze[0][self.reachVertice][0]-2 or self.pos[0]==self.Waze[0][self.reachVertice][0]+2) and self.pos[1]-self.Waze[0][self.reachVertice][1]>0:
                    if self.pos[0]-self.Waze[0][self.reachVertice][0]>0:
                        self.model.grid.move_agent(self,(x0-1,y0))
                    else:
                        self.model.grid.move_agent(self,(x0+1,y0))
                    #self.lastDirection="Down"
                elif (self.pos[1]==self.Waze[0][self.reachVertice][1]-2 or self.pos[1]==self.Waze[0][self.reachVertice][1]+2) and self.pos[0]-self.Waze[0][self.reachVertice][0]>0:
                    if self.pos[1]-self.Waze[0][self.reachVertice][1]>0:
                        self.model.grid.move_agent(self,(x0,y0-1))
                    else:
                        self.model.grid.move_agent(self,(x0,y0+1))
                    #self.lastDirection="Left"
                elif (self.pos[1]==self.Waze[0][self.reachVertice][1]-2 or self.pos[1]==self.Waze[0][self.reachVertice][1]+2) and self.pos[0]-self.Waze[0][self.reachVertice][0]<0:
                    if self.pos[1]-self.Waze[0][self.reachVertice][1]>0:
                        self.model.grid.move_agent(self,(x0,y0-1))
                    else:
                        self.model.grid.move_agent(self,(x0,y0+1))
                    #self.lastDirection="Right"
                    
        elif self.pos in self.Waze[0]:
            if self.pos==self.Waze[0][self.reachVertice]:
                self.reachVertice+=1
            if self.pos[0]==self.Waze[0][self.reachVertice][0]:
                if self.pos[1]-self.Waze[0][self.reachVertice][1]>0:
                    print("Enttra para moverse abajo de:")
                    print(self.pos)
                    self.model.grid.move_agent(self,(x0,y0-1))
                    self.lastDirection="Down"
                    print("Llego a ")
                    print(self.pos)
                elif self.pos[1]-self.Waze[0][self.reachVertice][1]<0:
                    print("Enttra para moverse arriba de:")
                    print(self.pos)
                    self.model.grid.move_agent(self,(x0,y0+1))
                    self.lastDirection="Up"
                    print("Llego a ")
                    print(self.pos)
            elif self.pos[1]==self.Waze[0][self.reachVertice][1]:
                if self.pos[0]-self.Waze[0][self.reachVertice][0]>0:
                    print("Enttra para moverse izq de:")
                    print(self.pos)
                    self.model.grid.move_agent(self,(x0-1,y0))
                    self.lastDirection="Left"
                    print("Llego a ")
                    print(self.pos)
                elif self.pos[0]-self.Waze[0][self.reachVertice][0]<0:
                    print("Enttra para moverse DER de:")
                    print(self.pos)
                    self.model.grid.move_agent(self,(x0+1,y0))
                    self.lastDirection="Right"
                    print("Aqui se movio")
                    print(self.pos)
                
        elif len(direccionRoad)>0:
            #Direcciones para Left,Right,Up y Down
            if direccionRoad[0].direction=="Left":
                self.model.grid.move_agent(self,(x0-1,y0))
                self.lastDirection="Left"
            elif direccionRoad[0].direction=="Right":
                self.model.grid.move_agent(self,(x0+1,y0))
                self.lastDirection="Right"
            elif direccionRoad[0].direction=="Up":
                self.model.grid.move_agent(self,(x0,y0+1))
                self.lastDirection="Up"
            elif direccionRoad[0].direction=="Down":
                self.model.grid.move_agent(self,(x0,y0-1))
                self.lastDirection="Down"
                
            #if self.pos == self.Waze[0][self.reachVertice]:
             #   self.reachVertice+=1
              #  break

        else:
            #LastDir para Left, Right, Up, Down
            if self.lastDirection=="Left" and goOrStop[0].state:
                self.model.grid.move_agent(self,(x0-1,y0))
            elif self.lastDirection=="Right" and goOrStop[0].state:
                self.model.grid.move_agent(self,(x0+1,y0))
            elif self.lastDirection=="Up" and goOrStop[0].state:
                self.model.grid.move_agent(self,(x0,y0+1))
            elif self.lastDirection=="Down" and goOrStop[0].state:
                self.model.grid.move_agent(self,(x0,y0-1))
        """
        if x0 != xf:
            direccion = -1 if xf - x0 < 0 else 1 #direccion
            self.model.grid.move_agent(self,(x0 + direccion,y0))
            #self.model.grid.move_agent(self,(x + direccion,y))
            return
        
        elif y0 != 1:
            direccion = -1 if 1 - y0 < 0 else 1 #direccion
            self.model.grid.move_agent(self,(x0,y0 + direccion))
            return
       
        self.model.grid.move_agent(self)
        """
    def choque(self):
        a = 0
        #if self.pos == next_agent.pos:
            #

    def step(self):
        """ 
        Determines the new direction it will take, and then moves
        """
        print(self.destination)
        if self.pos==self.destination:
            ##Aqui se destruye el objeto
            print("Prueba XD")
        else:
            self.move()

class Traffic_Light(Agent):
    """
    Traffic light. Where the traffic lights are in the grid.
    """
    def __init__(self, unique_id, model, state = False, timeToChange = 5):
        super().__init__(unique_id, model)
        """
        Creates a new Traffic light.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
            state: Whether the traffic light is green or red
            timeToChange: After how many step should the traffic light change color 
        """
        self.state = state
        self.timeToChange = timeToChange

    def step(self):
        """ 
        To change the state (green or red) of the traffic light in case you consider the time to change of each traffic light.
        """
        # if self.model.schedule.steps % self.timeToChange == 0:
        #     self.state = not self.state
        pass

class Destination(Agent):
    """
    Destination agent. Where each car should go.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class Obstacle(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class Road(Agent):
    """
    Road agent. Determines where the cars can move, and in which direction.
    """
    def __init__(self, unique_id, model, direction= "Left"):
        """
        Creates a new road.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
            direction: Direction where the cars can move
        """
        super().__init__(unique_id, model)
        self.direction = direction

    def step(self):
        pass
