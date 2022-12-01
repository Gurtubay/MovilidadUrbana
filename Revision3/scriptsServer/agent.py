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
        self.vision=[(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0)]
        self.breakLights=False
        #self.knowledge1=[(pos),obj] <- SENSORES
        
    def justMoveIf(self):
        outIndex=False
        outIndex1=False
        outIndex2=False
        if self.vision[0][0]>=0 and self.vision[0][0] <=23 and self.vision[0][1] >=0 and self.vision[0][1] <=24:
            position =self.model.grid.get_cell_list_contents(self.vision[0])
            cocheDelante=[obj for obj in position if isinstance(obj,Car)]
            outIndex=True
            
        if self.vision[3][0]>=0 and self.vision[3][0] <=23 and self.vision[3][1] >=0 and self.vision[3][1] <=24:
            position2 =self.model.grid.get_cell_list_contents(self.vision[3])
            cocheDelante2=[obj for obj in position2 if isinstance(obj,Car)]
            outIndex1=True
            
        if self.vision[6][0]>=0 and self.vision[6][0] <=23 and self.vision[6][1] >=0 and self.vision[6][1] <=24:
            position3 =self.model.grid.get_cell_list_contents(self.vision[6])
            cocheDelante3=[obj for obj in position3 if isinstance(obj,Car)]
            outIndex2=True
            
        if outIndex and outIndex1 and outIndex2:    
            if len(cocheDelante)==0 and (len(cocheDelante2)==0 or cocheDelante2[0].lastDirection != "Down") and (len(cocheDelante3)==0 or cocheDelante3[0].lastDirection != "Up") and self.lastDirection=="Right":
                return True
            elif len(cocheDelante)==0 and (len(cocheDelante2)==0 or cocheDelante2[0].lastDirection != "Down") and (len(cocheDelante3)==0 or cocheDelante3[0].lastDirection != "Up") and self.lastDirection=="Left":
                return True
            elif len(cocheDelante)==0 and self.lastDirection=="Up":
                return True
            elif len(cocheDelante)==0 and self.lastDirection=="Down":
                return True
            
        elif outIndex and outIndex1:
            if len(cocheDelante)==0 and (len(cocheDelante2)==0 or cocheDelante2[0].lastDirection != "Down") and self.lastDirection=="Right":
                return True
            elif len(cocheDelante)==0 and (len(cocheDelante2)==0 or cocheDelante2[0].lastDirection != "Down") and self.lastDirection=="Left":
                return True
            elif len(cocheDelante)==0 and self.lastDirection=="Up":
                return True
            elif len(cocheDelante)==0 and self.lastDirection=="Down":
                return True
            
        elif outIndex and outIndex2:
            if len(cocheDelante)==0 and (len(cocheDelante3)==0 or cocheDelante3[0].lastDirection != "Up") and self.lastDirection=="Right":
                return True
            elif len(cocheDelante)==0 and (len(cocheDelante3)==0 or cocheDelante3[0].lastDirection != "Up") and self.lastDirection=="Left":
                return True
            elif len(cocheDelante)==0 and self.lastDirection=="Up":
                return True
            elif len(cocheDelante)==0 and self.lastDirection=="Down":
                return True
        
        
    def setVision(self):
        if self.lastDirection=="Left":
            self.vision[0]=(self.pos[0]-1,self.pos[1])
            self.vision[1]=(self.pos[0]-2,self.pos[1])
            self.vision[2]=(self.pos[0]-3,self.pos[1])
            self.vision[3]=(self.pos[0]-1,self.pos[1]+1)
            self.vision[4]=(self.pos[0]-2,self.pos[1]+1)
            self.vision[5]=(self.pos[0]-3,self.pos[1]+1)
            self.vision[6]=(self.pos[0]-1,self.pos[1]-1)
            self.vision[7]=(self.pos[0]-2,self.pos[1]-1)
            self.vision[8]=(self.pos[0]-3,self.pos[1]-1)
            self.vision[9]=(self.pos[0],self.pos[1]+1)
            self.vision[10]=(self.pos[0],self.pos[1]-1)
            
        elif self.lastDirection=="Right":
            print("Reajuste")
            self.vision[0]=(self.pos[0]+1,self.pos[1])
            self.vision[1]=(self.pos[0]+2,self.pos[1])
            self.vision[2]=(self.pos[0]+3,self.pos[1])
            self.vision[3]=(self.pos[0]+1,self.pos[1]+1)
            self.vision[4]=(self.pos[0]+2,self.pos[1]+1)
            self.vision[5]=(self.pos[0]+3,self.pos[1]+1)
            self.vision[6]=(self.pos[0]+1,self.pos[1]-1)
            self.vision[7]=(self.pos[0]+2,self.pos[1]-1)
            self.vision[8]=(self.pos[0]+3,self.pos[1]-1)
            self.vision[9]=(self.pos[0],self.pos[1]+1)
            self.vision[10]=(self.pos[0],self.pos[1]-1)
            
        elif self.lastDirection=="Up":
            self.vision[0]=(self.pos[0],self.pos[1]+1)
            self.vision[1]=(self.pos[0],self.pos[1]+2)
            self.vision[2]=(self.pos[0],self.pos[1]+3)
            self.vision[3]=(self.pos[0]+1,self.pos[1]+1)
            self.vision[4]=(self.pos[0]+1,self.pos[1]+2)
            self.vision[5]=(self.pos[0]+1,self.pos[1]+3)
            self.vision[6]=(self.pos[0]-1,self.pos[1]+1)
            self.vision[7]=(self.pos[0]-1,self.pos[1]+2)
            self.vision[8]=(self.pos[0]-1,self.pos[1]+3)
            self.vision[9]=(self.pos[0]+1,self.pos[1])
            self.vision[10]=(self.pos[0]-1,self.pos[1])
            
        elif self.lastDirection=="Down":
            self.vision[0]=(self.pos[0],self.pos[1]-1)
            self.vision[1]=(self.pos[0],self.pos[1]-2)
            self.vision[2]=(self.pos[0],self.pos[1]-3)
            self.vision[3]=(self.pos[0]+1,self.pos[1]-1)
            self.vision[4]=(self.pos[0]+1,self.pos[1]-2)
            self.vision[5]=(self.pos[0]+1,self.pos[1]-3)
            self.vision[6]=(self.pos[0]-1,self.pos[1]-1)
            self.vision[7]=(self.pos[0]-1,self.pos[1]-2)
            self.vision[8]=(self.pos[0]-1,self.pos[1]-3)
            self.vision[9]=(self.pos[0]+1,self.pos[1])
            self.vision[10]=(self.pos[0]-1,self.pos[1])
            
        
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
        #print(str(self.unique_id) +"|"+ str(self.Waze))
        #print(str(self.unique_id) +"|" +str(self.pos))
        #print(str(self.unique_id)+ "|" +str(self.Waze[0][self.reachVertice]))
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
                #print("Ultima recta!!!!!!")
                if (self.pos[0]==self.Waze[0][self.reachVertice][0]-1 or self.pos[0]==self.Waze[0][self.reachVertice][0]+1) and self.pos[1]-self.Waze[0][self.reachVertice][1]<0:
                    if self.justMoveIf():
                        self.model.grid.move_agent(self,(x0,y0+1))
                    #print("Finalmente hacia arriba")
                    self.lastDirection="Up"
                elif (self.pos[0]==self.Waze[0][self.reachVertice][0]-1 or self.pos[0]==self.Waze[0][self.reachVertice][0]+1) and self.pos[1]-self.Waze[0][self.reachVertice][1]>0:
                    if self.justMoveIf():
                        self.model.grid.move_agent(self,(x0,y0-1))
                    #print("Finalmente hacia abajo")
                    self.lastDirection="Down"
                elif (self.pos[1]==self.Waze[0][self.reachVertice][1]-1 or self.pos[1]==self.Waze[0][self.reachVertice][1]+1) and self.pos[0]-self.Waze[0][self.reachVertice][0]>0:
                    if self.justMoveIf():
                        self.model.grid.move_agent(self,(x0-1,y0))
                    #print("Finalmente hacia Izq")
                    self.lastDirection="Left"
                elif (self.pos[1]==self.Waze[0][self.reachVertice][1]-1 or self.pos[1]==self.Waze[0][self.reachVertice][1]+1) and self.pos[0]-self.Waze[0][self.reachVertice][0]<0:
                    if self.justMoveIf():
                        self.model.grid.move_agent(self,(x0+1,y0))
                    #print("Finalmente hacia Der")
                    self.lastDirection="Right"
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
                    #print("Enttra para moverse abajo de:")
                    #print(self.pos)
                    if self.justMoveIf():
                        self.model.grid.move_agent(self,(x0,y0-1))
                    self.lastDirection="Down"
                    #print("Llego a ")
                    #print(self.pos)
                elif self.pos[1]-self.Waze[0][self.reachVertice][1]<0:
                    #print("Enttra para moverse arriba de:")
                    #print(self.pos)
                    if self.justMoveIf():
                        self.model.grid.move_agent(self,(x0,y0+1))
                    self.lastDirection="Up"
                    #print("Llego a ")
                    #print(self.pos)
            elif self.pos[1]==self.Waze[0][self.reachVertice][1]:
                if self.pos[0]-self.Waze[0][self.reachVertice][0]>0:
                    #print("Enttra para moverse izq de:")
                    #print(self.pos)
                    if self.justMoveIf():
                        self.model.grid.move_agent(self,(x0-1,y0))
                    self.lastDirection="Left"
                    #print("Llego a ")
                    #print(self.pos)
                elif self.pos[0]-self.Waze[0][self.reachVertice][0]<0:
                    #print("Enttra para moverse DER de:")
                    #print(self.pos)
                    if self.justMoveIf():
                        self.model.grid.move_agent(self,(x0+1,y0))
                    self.lastDirection="Right"
                    #print("Aqui se movio")
                    #print(self.pos)
                
        elif len(direccionRoad)>0:
            #Direcciones para Left,Right,Up y Down
            if direccionRoad[0].direction=="Left":
                if self.justMoveIf():
                    self.model.grid.move_agent(self,(x0-1,y0))
                    self.lastDirection="Left"
            elif direccionRoad[0].direction=="Right":
                if self.justMoveIf():
                    self.model.grid.move_agent(self,(x0+1,y0))
                    self.lastDirection="Right"
            elif direccionRoad[0].direction=="Up":
                if self.justMoveIf():
                    self.model.grid.move_agent(self,(x0,y0+1))
                    self.lastDirection="Up"
            elif direccionRoad[0].direction=="Down":
                if self.justMoveIf():
                    self.model.grid.move_agent(self,(x0,y0-1))
                    self.lastDirection="Down"
                
            #if self.pos == self.Waze[0][self.reachVertice]:
             #   self.reachVertice+=1
              #  break

        else:
            #LastDir para Left, Right, Up, Down
            if self.lastDirection=="Left" and goOrStop[0].state:
                if self.justMoveIf():
                    self.model.grid.move_agent(self,(x0-1,y0))
            elif self.lastDirection=="Right" and goOrStop[0].state:
                if self.justMoveIf():
                    self.model.grid.move_agent(self,(x0+1,y0))
            elif self.lastDirection=="Up" and goOrStop[0].state:
                if self.justMoveIf():
                    self.model.grid.move_agent(self,(x0,y0+1))
            elif self.lastDirection=="Down" and goOrStop[0].state:
                if self.justMoveIf():
                    self.model.grid.move_agent(self,(x0,y0-1))

    def choque(self):
        a = 0
        #if self.pos == next_agent.pos:
            #

    def step(self):
        """ 
        Determines the new direction it will take, and then moves
        """
        self.setVision()
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
