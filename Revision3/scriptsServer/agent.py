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
        backAmpel=False
        rotondaPos=[(12,11),(13,11),(17,11),(18,11),(12,9),(13,9),(17,9),(18,9)]
        if self.lastDirection=="Left":
            position =self.model.grid.get_cell_list_contents([self.pos])
            goOrStop = [obj for obj in position if isinstance(obj,Traffic_Light)]
            if len(goOrStop)>0:
                backAmpel=True
        elif self.lastDirection=="Right":
            position =self.model.grid.get_cell_list_contents([self.pos])
            goOrStop = [obj for obj in position if isinstance(obj,Traffic_Light)]
            if len(goOrStop)>0:
                backAmpel=True
        elif self.lastDirection=="Down":
            position =self.model.grid.get_cell_list_contents([self.pos])
            goOrStop = [obj for obj in position if isinstance(obj,Traffic_Light)]
            if len(goOrStop)>0:
                backAmpel=True
        elif self.lastDirection=="Up":
            position =self.model.grid.get_cell_list_contents([self.pos])
            goOrStop = [obj for obj in position if isinstance(obj,Traffic_Light)]
            if len(goOrStop)>0:
                backAmpel=True
            
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
        print(str(outIndex)+"Delante")
        print(str(outIndex)+"Der")
        print(str(outIndex)+"Izq")
        
        if outIndex and backAmpel:    
            if len(cocheDelante)==0:
                return True
                
        elif outIndex and outIndex1 and outIndex2:    
            if (len(cocheDelante)==0 and (len(cocheDelante2)==0 or cocheDelante2[0].lastDirection != "Down") and (len(cocheDelante3)==0 or cocheDelante3[0].lastDirection != "Up") and self.lastDirection=="Right") or self.pos in rotondaPos:
                return True
            elif (len(cocheDelante)==0 and (len(cocheDelante2)==0 or cocheDelante2[0].lastDirection != "Up") and (len(cocheDelante3)==0 or cocheDelante3[0].lastDirection != "Down") and self.lastDirection=="Left") or self.pos in rotondaPos:
                return True
            elif (len(cocheDelante)==0 and (len(cocheDelante2)==0 or cocheDelante2[0].lastDirection != "Right") and (len(cocheDelante3)==0 or cocheDelante3[0].lastDirection != "Left") and self.lastDirection=="Up") or self.pos in rotondaPos:
                return True
            elif (len(cocheDelante)==0 and (len(cocheDelante2)==0 or cocheDelante2[0].lastDirection != "Left") and (len(cocheDelante3)==0 or cocheDelante3[0].lastDirection != "Right") and self.lastDirection=="Down") or self.pos in rotondaPos:
                return True
            
        elif outIndex and outIndex1:
            if (len(cocheDelante)==0 and (len(cocheDelante2)==0 or cocheDelante2[0].lastDirection != "Down") and self.lastDirection=="Right") or self.pos in rotondaPos:
                return True
            elif (len(cocheDelante)==0 and (len(cocheDelante2)==0 or cocheDelante2[0].lastDirection != "Up") and self.lastDirection=="Left") or self.pos in rotondaPos:
                return True
            elif (len(cocheDelante)==0 and (len(cocheDelante2)==0 or cocheDelante2[0].lastDirection != "Right") and self.lastDirection=="Up") or self.pos in rotondaPos:
                return True
            elif (len(cocheDelante)==0 and (len(cocheDelante2)==0 or cocheDelante2[0].lastDirection != "Left") and self.lastDirection=="Down") or self.pos in rotondaPos:
                return True
            
        elif outIndex and outIndex2:
            if (len(cocheDelante)==0 and (len(cocheDelante3)==0 or cocheDelante3[0].lastDirection != "Up") and self.lastDirection=="Right") or self.pos in rotondaPos:
                return True
            elif (len(cocheDelante)==0 and (len(cocheDelante3)==0 or cocheDelante3[0].lastDirection != "Down") and self.lastDirection=="Left") or self.pos in rotondaPos:
                return True
            elif (len(cocheDelante)==0 and (len(cocheDelante3)==0 or cocheDelante3[0].lastDirection != "Left") and self.lastDirection=="Up") or self.pos in rotondaPos:
                return True
            elif (len(cocheDelante)==0 and (len(cocheDelante3)==0 or cocheDelante3[0].lastDirection != "Right") and self.lastDirection=="Down") or self.pos in rotondaPos:
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
            if self.lastDirection=="Left" and goOrStop[0].state=="green":
                if self.justMoveIf():
                    self.model.grid.move_agent(self,(x0-1,y0))
            elif self.lastDirection=="Right" and goOrStop[0].state=="green":
                if self.justMoveIf():
                    self.model.grid.move_agent(self,(x0+1,y0))
            elif self.lastDirection=="Up" and goOrStop[0].state=="green":
                if self.justMoveIf():
                    self.model.grid.move_agent(self,(x0,y0+1))
            elif self.lastDirection=="Down" and goOrStop[0].state=="green":
                if self.justMoveIf():
                    self.model.grid.move_agent(self,(x0,y0-1))


    def step(self):
        """ 
        Determines the new direction it will take, and then moves
        """
        self.setVision()
#         print(self.destination)
        if self.pos==self.destination:
            ##Aqui se destruye el objeto
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
        else:
            self.move()

class Traffic_Light(Agent):
    """
    Traffic light. Where the traffic lights are in the grid.
    """
    def __init__(self, unique_id, model, state = "red",roadMap=[]):
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
        self.countStep = 0
        self.unique_id = unique_id
        self.vision=[(0,0),(0,0),(0,0)]
        self.roadMap=roadMap
        self.neighbour=[]
        self.brother=None
        self.carsPool=0
        self.weight=1
#         if self.state == "red":
#             self.currentStep = 10
        
    def ampelLogic(self):
        position =self.model.grid.get_cell_list_contents(self.vision[0])
        carWaiting1=[obj for obj in position if isinstance(obj,Car)]
        position =self.model.grid.get_cell_list_contents(self.vision[1])
        carWaiting2=[obj for obj in position if isinstance(obj,Car)]
        position =self.model.grid.get_cell_list_contents(self.vision[2])
        carWaiting3=[obj for obj in position if isinstance(obj,Car)]
        
        position =self.model.grid.get_cell_list_contents(self.pos)
        carWaiting=[obj for obj in position if isinstance(obj,Car)]
        position0 =self.model.grid.get_cell_list_contents(self.brother.pos)
        carWaiting0=[obj for obj in position0 if isinstance(obj,Car)]
        position2 =self.model.grid.get_cell_list_contents(self.neighbour[0].pos)
        carNei1=[obj for obj in position2 if isinstance(obj,Car)]
        position3 =self.model.grid.get_cell_list_contents(self.neighbour[0].pos)
        carNei2=[obj for obj in position3 if isinstance(obj,Car)]
            
        if (self.state=="yellow" and self.neighbour[0].state=="yellow" and len(carWaiting3)>0) or len(carWaiting)>0:
            self.state="green"
            self.brother.state="green"
            self.neighbour[0].state="red"
            self.neighbour[1].state="red"
            self.carsPool=1
            
        elif self.state=="red" and self.neighbour[0].carsPool==0 and self.neighbour[1].carsPool==0:
            position =self.model.grid.get_cell_list_contents(self.pos)
            carWaiting=[obj for obj in position if isinstance(obj,Car)]
            position0 =self.model.grid.get_cell_list_contents(self.brother.pos)
            carWaiting0=[obj for obj in position0 if isinstance(obj,Car)]
            position2 =self.model.grid.get_cell_list_contents(self.neighbour[0].pos)
            carNei1=[obj for obj in position2 if isinstance(obj,Car)]
            position3 =self.model.grid.get_cell_list_contents(self.neighbour[0].pos)
            carNei2=[obj for obj in position3 if isinstance(obj,Car)]
            if self.carsPool==0 and self.brother.carsPool==0 and len(carWaiting)==0 and len(carNei1)==0 and len(carNei2)==0 and len(carWaiting0)==0:
                self.state="yellow"
                self.brother.state="yellow"
                self.neighbour[0].state="yellow"
                self.neighbour[1].state="yellow"               
            else:
                self.state="green"
                self.brother.state="green"
                self.neighbour[0].state="red"
                self.neighbour[1].state="red"
                self.countStep=1
                self.neighbour[0].weight=1
                self.neighbour[1].weight=1
        elif len(carWaiting1)==0 and len(carWaiting2)==0 and len(carWaiting3)==0:
            self.carsPool=0
            
        elif len(carWaiting1)==1 and len(carWaiting2)==1 and len(carWaiting3)==1 and self.state=="green":
            self.carsPool=3
            position =self.model.grid.get_cell_list_contents(self.pos)
            carPassing=[obj for obj in position if isinstance(obj,Car)]
            if len(carPassing)>0:
                self.weight-=1
        elif len(carWaiting1)==1 and len(carWaiting2)==0 and len(carWaiting3)==1 and self.state=="green":
            self.carsPool=2
            position =self.model.grid.get_cell_list_contents(self.pos)
            carPassing=[obj for obj in position if isinstance(obj,Car)]
            if len(carPassing)>0:
                self.weight-=1
        elif len(carWaiting1)==1 and len(carWaiting2)==1 and len(carWaiting3)==0 and self.state=="green":
            self.carsPool=2
            position =self.model.grid.get_cell_list_contents(self.pos)
            carPassing=[obj for obj in position if isinstance(obj,Car)]
            if len(carPassing)>0:
                self.weight-=1
        elif len(carWaiting1)==0 and len(carWaiting2)==1 and len(carWaiting3)==1 and self.state=="green":
            self.carsPool=2
            position =self.model.grid.get_cell_list_contents(self.pos)
            carPassing=[obj for obj in position if isinstance(obj,Car)]
            if len(carPassing)>0:
                self.weight-=1
        elif len(carWaiting1)==0 and len(carWaiting2)==0 and len(carWaiting3)==1 and self.state=="green":
            self.carsPool=1
            position =self.model.grid.get_cell_list_contents(self.pos)
            carPassing=[obj for obj in position if isinstance(obj,Car)]
            if len(carPassing)>0:
                self.weight-=1
        elif len(carWaiting1)==0 and len(carWaiting2)==1 and len(carWaiting3)==0 and self.state=="green":
            self.carsPool=1
            position =self.model.grid.get_cell_list_contents(self.pos)
            carPassing=[obj for obj in position if isinstance(obj,Car)]
            if len(carPassing)>0:
                self.weight-=1
        elif len(carWaiting1)==1 and len(carWaiting2)==0 and len(carWaiting3)==0 and self.state=="green":
            self.carsPool=1
            position =self.model.grid.get_cell_list_contents(self.pos)
            carPassing=[obj for obj in position if isinstance(obj,Car)]
            if len(carPassing)>0:
                self.weight-=1
            
        elif len(carWaiting1)==1 and len(carWaiting2)==1 and len(carWaiting3)==1 and self.state=="red":
            self.carsPool=3
            self.weight+=self.carsPool*self.countStep
            self.countStep+=1
            if self.weight+self.brother.weight>=self.neighbour[0].weight+self.neighbour[1].weight:
                self.state="green"
                self.brother.state="green"
                self.neighbour[0].state="red"
                self.neighbour[1].state="red"
                self.countStep=1
                self.neighbour[0].weight=1
                self.neighbour[1].weight=1
        elif len(carWaiting1)==1 and len(carWaiting2)==0 and len(carWaiting3)==1 and self.state=="red":
            self.carsPool=2
            self.weight+=self.carsPool*self.countStep
            self.countStep+=1
            if self.weight+self.brother.weight>=self.neighbour[0].weight+self.neighbour[1].weight:
                self.state="green"
                self.brother.state="green"
                self.neighbour[0].state="red"
                self.neighbour[1].state="red"
                self.countStep=1
                self.neighbour[0].weight=1
                self.neighbour[1].weight=1
        elif len(carWaiting1)==1 and len(carWaiting2)==1 and len(carWaiting3)==0 and self.state=="red":
            self.carsPool=2
            self.weight+=self.carsPool*self.countStep
            self.countStep+=1
            if self.weight+self.brother.weight>=self.neighbour[0].weight+self.neighbour[1].weight:
                self.state="green"
                self.brother.state="green"
                self.neighbour[0].state="red"
                self.neighbour[1].state="red"
                self.countStep=1
                self.neighbour[0].weight=1
                self.neighbour[1].weight=1
        elif len(carWaiting1)==0 and len(carWaiting2)==1 and len(carWaiting3)==1 and self.state=="red":
            self.carsPool=2
            self.weight+=self.carsPool*self.countStep
            self.countStep+=1
            if self.weight+self.brother.weight>=self.neighbour[0].weight+self.neighbour[1].weight:
                self.state="green"
                self.brother.state="green"
                self.neighbour[0].state="red"
                self.neighbour[1].state="red"
                self.countStep=1
                self.neighbour[0].weight=1
                self.neighbour[1].weight=1
        elif len(carWaiting1)==0 and len(carWaiting2)==0 and len(carWaiting3)==1 and self.state=="red":
            self.carsPool=1
            self.weight+=self.carsPool*self.countStep
            self.countStep+=1
            if self.weight+self.brother.weight>=self.neighbour[0].weight+self.neighbour[1].weight:
                self.state="green"
                self.brother.state="green"
                self.neighbour[0].state="red"
                self.neighbour[1].state="red"
                self.countStep=1
                self.neighbour[0].weight=1
                self.neighbour[1].weight=1
        elif len(carWaiting1)==0 and len(carWaiting2)==1 and len(carWaiting3)==0 and self.state=="red":
            self.carsPool=1
            self.weight+=self.carsPool*self.countStep
            self.countStep+=1
            if self.weight+self.brother.weight>=self.neighbour[0].weight+self.neighbour[1].weight:
                self.state="green"
                self.brother.state="green"
                self.neighbour[0].state="red"
                self.neighbour[1].state="red"
                self.countStep=1
                self.neighbour[0].weight=1
                self.neighbour[1].weight=1
        elif len(carWaiting1)==1 and len(carWaiting2)==0 and len(carWaiting3)==0 and self.state=="red":
            self.carsPool=1
            self.weight+=self.carsPool*self.countStep
            self.countStep+=1
            if self.weight+self.brother.weight>=self.neighbour[0].weight+self.neighbour[1].weight:
                self.state="green"
                self.brother.state="green"
                self.neighbour[0].state="red"
                self.neighbour[1].state="red"
                self.countStep=1
                self.neighbour[0].weight=1
                self.neighbour[1].weight=1
            
        
        
    def setSensor(self):
        if [(self.pos[0]+1, self.pos[1]), "Left"] in self.roadMap:
            self.vision[0]=(self.pos[0]+1, self.pos[1])
            self.vision[1]=(self.pos[0]+2, self.pos[1])
            self.vision[2]=(self.pos[0]+3, self.pos[1])
            
#             Set del hermano
            if self.pos[0] >=0 and self.pos[1]+1 >=0 and self.pos[0] <=23 and self.pos[1]+1<=24:
                position =self.model.grid.get_cell_list_contents((self.pos[0], self.pos[1]+1))
                ampelBrother=[obj for obj in position if isinstance(obj,Traffic_Light)]
                if len(ampelBrother)>0:
                    self.brother=ampelBrother[0]
            if self.pos[0] >=0 and self.pos[1]-1 >=0 and self.pos[0] <=23 and self.pos[1]-1<=24:
                position =self.model.grid.get_cell_list_contents((self.pos[0], self.pos[1]-1))
                ampelBrother=[obj for obj in position if isinstance(obj,Traffic_Light)]
                if len(ampelBrother)>0:
                    self.brother=ampelBrother[0]
                
#           Arriba Derecha
            if self.pos[0]+1 >=0 and self.pos[1]+1 >=0 and self.pos[0]+1 <=23 and self.pos[1]+1<=24:
                position =self.model.grid.get_cell_list_contents((self.pos[0]+1, self.pos[1]+1))
                ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                if len(ampelVecino)>0:
                    self.neighbour.append(ampelVecino[0])
                    position =self.model.grid.get_cell_list_contents((self.pos[0]+2, self.pos[1]+1))
                    ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                    self.neighbour.append(ampelVecino[0])
                
#            Arriba Izquierda
            if self.pos[0]-1 >=0 and self.pos[1]+1 >=0 and self.pos[0]-1 <=23 and self.pos[1]+1<=24:
                position =self.model.grid.get_cell_list_contents((self.pos[0]-1, self.pos[1]+1))
                ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                if len(ampelVecino)>0:
                    self.neighbour.append(ampelVecino[0])
                    position =self.model.grid.get_cell_list_contents((self.pos[0]-2, self.pos[1]+1))
                    ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                    self.neighbour.append(ampelVecino[0])
             
#           Abajo Derecha
            if self.pos[0]+1 >=0 and self.pos[1]-1 >=0 and self.pos[0]+1 <=23 and self.pos[1]-1<=24:
                position =self.model.grid.get_cell_list_contents((self.pos[0]+1, self.pos[1]-1))
                ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                if len(ampelVecino)>0:
                    self.neighbour.append(ampelVecino[0])
                    position =self.model.grid.get_cell_list_contents((self.pos[0]+2, self.pos[1]-1))
                    ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                    self.neighbour.append(ampelVecino[0])
            
#           Abajo Izquierda
            if self.pos[0]-1 >=0 and self.pos[1]-1 >=0 and self.pos[0]-1 <=23 and self.pos[1]-1<=24:
                position =self.model.grid.get_cell_list_contents((self.pos[0]-1, self.pos[1]-1))
                ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                if len(ampelVecino)>0:
                    self.neighbour.append(ampelVecino[0])
                    position =self.model.grid.get_cell_list_contents((self.pos[0]-2, self.pos[1]-1))
                    ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                    self.neighbour.append(ampelVecino[0])
            
#           2 Arriba Derecha
            if self.pos[0]+1 >=0 and self.pos[1]+2 >=0 and self.pos[0]+1 <=23 and self.pos[1]+2<=24:
                position =self.model.grid.get_cell_list_contents((self.pos[0]+1, self.pos[1]+2))
                ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                if len(ampelVecino)>0:
                    self.neighbour.append(ampelVecino[0])
                    position =self.model.grid.get_cell_list_contents((self.pos[0]+2, self.pos[1]+2))
                    ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                    self.neighbour.append(ampelVecino[0])
             
#           2 Arriba Izquierda
            if self.pos[0]-1 >=0 and self.pos[1]+2 >=0 and self.pos[0]-1 <=23 and self.pos[1]+2<=24:
                position =self.model.grid.get_cell_list_contents((self.pos[0]-1, self.pos[1]+2))
                ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                if len(ampelVecino)>0:
                    self.neighbour.append(ampelVecino[0])
                    position =self.model.grid.get_cell_list_contents((self.pos[0]-2, self.pos[1]+2))
                    ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                    self.neighbour.append(ampelVecino[0])
                
#           2 Abajo Derecha
            if self.pos[0]+1 >=0 and self.pos[1]-2 >=0 and self.pos[0]+1 <=23 and self.pos[1]+2<=24:
                position =self.model.grid.get_cell_list_contents((self.pos[0]+1, self.pos[1]-2))
                ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                if len(ampelVecino)>0:
                    self.neighbour.append(ampelVecino[0])
                    position =self.model.grid.get_cell_list_contents((self.pos[0]+2, self.pos[1]-2))
                    ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                    self.neighbour.append(ampelVecino[0])
                
#           2 Abajo Izquierda
            if self.pos[0]-1 >=0 and self.pos[1]-2 >=0 and self.pos[0]-1 <=23 and self.pos[1]-2<=24:
                position =self.model.grid.get_cell_list_contents((self.pos[0]-1, self.pos[1]-2))
                ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                if len(ampelVecino)>0:
                    self.neighbour.append(ampelVecino[0])
                    position =self.model.grid.get_cell_list_contents((self.pos[0]-2, self.pos[1]-2))
                    ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                    self.neighbour.append(ampelVecino[0])
            
        elif [(self.pos[0]-1, self.pos[1]), "Right"] in self.roadMap:
            self.vision[0]=(self.pos[0]-1, self.pos[1])
            self.vision[1]=(self.pos[0]-2, self.pos[1])
            self.vision[2]=(self.pos[0]-3, self.pos[1])
#             Set del hermano
            if self.pos[0] >=0 and self.pos[1]+1 >=0 and self.pos[0] <=23 and self.pos[1]+1<=24:
                position =self.model.grid.get_cell_list_contents((self.pos[0], self.pos[1]+1))
                ampelBrother=[obj for obj in position if isinstance(obj,Traffic_Light)]
                if len(ampelBrother)>0:
                    self.brother=ampelBrother[0]
            if self.pos[0] >=0 and self.pos[1]-1 >=0 and self.pos[0] <=23 and self.pos[1]-1<=24:
                position =self.model.grid.get_cell_list_contents((self.pos[0], self.pos[1]-1))
                ampelBrother=[obj for obj in position if isinstance(obj,Traffic_Light)]
                if len(ampelBrother)>0:
                    self.brother=ampelBrother[0]
                
#           Arriba Derecha
            if self.pos[0]+1 >=0 and self.pos[1]+1 >=0 and self.pos[0]+1 <=23 and self.pos[1]+1<=24:
                position =self.model.grid.get_cell_list_contents((self.pos[0]+1, self.pos[1]+1))
                ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                if len(ampelVecino)>0:
                    self.neighbour.append(ampelVecino[0])
                    position =self.model.grid.get_cell_list_contents((self.pos[0]+2, self.pos[1]+1))
                    ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                    self.neighbour.append(ampelVecino[0])
                
#            Arriba Izquierda
            if self.pos[0]-1 >=0 and self.pos[1]+1 >=0 and self.pos[0]-1 <=23 and self.pos[1]+1<=24:
                position =self.model.grid.get_cell_list_contents((self.pos[0]-1, self.pos[1]+1))
                ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                if len(ampelVecino)>0:
                    self.neighbour.append(ampelVecino[0])
                    position =self.model.grid.get_cell_list_contents((self.pos[0]-2, self.pos[1]+1))
                    ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                    self.neighbour.append(ampelVecino[0])
             
#           Abajo Derecha
            if self.pos[0]+1 >=0 and self.pos[1]-1 >=0 and self.pos[0]+1 <=23 and self.pos[1]-1<=24:
                position =self.model.grid.get_cell_list_contents((self.pos[0]+1, self.pos[1]-1))
                ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                if len(ampelVecino)>0:
                    self.neighbour.append(ampelVecino[0])
                    position =self.model.grid.get_cell_list_contents((self.pos[0]+2, self.pos[1]-1))
                    ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                    self.neighbour.append(ampelVecino[0])
            
#           Abajo Izquierda
            if self.pos[0]-1 >=0 and self.pos[1]-1 >=0 and self.pos[0]-1 <=23 and self.pos[1]-1<=24:
                position =self.model.grid.get_cell_list_contents((self.pos[0]-1, self.pos[1]-1))
                ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                if len(ampelVecino)>0:
                    self.neighbour.append(ampelVecino[0])
                    position =self.model.grid.get_cell_list_contents((self.pos[0]-2, self.pos[1]-1))
                    ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                    self.neighbour.append(ampelVecino[0])
            
#           2 Arriba Derecha
            if self.pos[0]+1 >=0 and self.pos[1]+2 >=0 and self.pos[0]+1 <=23 and self.pos[1]+2<=24:
                position =self.model.grid.get_cell_list_contents((self.pos[0]+1, self.pos[1]+2))
                ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                if len(ampelVecino)>0:
                    self.neighbour.append(ampelVecino[0])
                    position =self.model.grid.get_cell_list_contents((self.pos[0]+2, self.pos[1]+2))
                    ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                    self.neighbour.append(ampelVecino[0])
             
#           2 Arriba Izquierda
            if self.pos[0]-1 >=0 and self.pos[1]+2 >=0 and self.pos[0]-1 <=23 and self.pos[1]+2<=24:
                position =self.model.grid.get_cell_list_contents((self.pos[0]-1, self.pos[1]+2))
                ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                if len(ampelVecino)>0:
                    self.neighbour.append(ampelVecino[0])
                    position =self.model.grid.get_cell_list_contents((self.pos[0]-2, self.pos[1]+2))
                    ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                    self.neighbour.append(ampelVecino[0])
                
#           2 Abajo Derecha
            if self.pos[0]+1 >=0 and self.pos[1]-2 >=0 and self.pos[0]+1 <=23 and self.pos[1]+2<=24:
                position =self.model.grid.get_cell_list_contents((self.pos[0]+1, self.pos[1]-2))
                ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                if len(ampelVecino)>0:
                    self.neighbour.append(ampelVecino[0])
                    position =self.model.grid.get_cell_list_contents((self.pos[0]+2, self.pos[1]-2))
                    ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                    self.neighbour.append(ampelVecino[0])
                
#           2 Abajo Izquierda
            if self.pos[0]-1 >=0 and self.pos[1]-2 >=0 and self.pos[0]-1 <=23 and self.pos[1]-2<=24:
                position =self.model.grid.get_cell_list_contents((self.pos[0]-1, self.pos[1]-2))
                ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                if len(ampelVecino)>0:
                    self.neighbour.append(ampelVecino[0])
                    position =self.model.grid.get_cell_list_contents((self.pos[0]-2, self.pos[1]-2))
                    ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                    self.neighbour.append(ampelVecino[0])

        elif [(self.pos[0], self.pos[1]+1), "Down"] in self.roadMap:
            self.vision[0]=(self.pos[0], self.pos[1]+1)
            self.vision[1]=(self.pos[0], self.pos[1]+2)
            self.vision[2]=(self.pos[0], self.pos[1]+3)
#             Set del hermano
            if self.pos[0]+1 >=0 and self.pos[1] >=0 and self.pos[0]+1 <=23 and self.pos[1]<=24:
                position =self.model.grid.get_cell_list_contents((self.pos[0]+1, self.pos[1]))
                ampelBrother=[obj for obj in position if isinstance(obj,Traffic_Light)]
                if len(ampelBrother)>0:
                    self.brother=ampelBrother[0]
            if self.pos[0]-1 >=0 and self.pos[1] >=0 and self.pos[0]-1 <=23 and self.pos[1]<=24:
                position =self.model.grid.get_cell_list_contents((self.pos[0]-1, self.pos[1]))
                ampelBrother=[obj for obj in position if isinstance(obj,Traffic_Light)]
                if len(ampelBrother)>0:
                    self.brother=ampelBrother[0]
                
#           Arriba Derecha
            if self.pos[0]+1 >=0 and self.pos[1]+1 >=0 and self.pos[0]+1 <=23 and self.pos[1]+1<=24:
                position =self.model.grid.get_cell_list_contents((self.pos[0]+1, self.pos[1]+1))
                ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                if len(ampelVecino)>0:
                    self.neighbour.append(ampelVecino[0])
                    position =self.model.grid.get_cell_list_contents((self.pos[0]+1, self.pos[1]+2))
                    ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                    self.neighbour.append(ampelVecino[0])
                
#            Arriba Izquierda
            if self.pos[0]-1 >=0 and self.pos[1]+1 >=0 and self.pos[0]-1 <=23 and self.pos[1]+1<=24:
                position =self.model.grid.get_cell_list_contents((self.pos[0]-1, self.pos[1]+1))
                ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                if len(ampelVecino)>0:
                    self.neighbour.append(ampelVecino[0])
                    position =self.model.grid.get_cell_list_contents((self.pos[0]-1, self.pos[1]+2))
                    ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                    self.neighbour.append(ampelVecino[0])
             
#           Abajo Derecha
            if self.pos[0]+1 >=0 and self.pos[1]-1 >=0 and self.pos[0]+1 <=23 and self.pos[1]-1<=24:
                position =self.model.grid.get_cell_list_contents((self.pos[0]+1, self.pos[1]-1))
                ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                if len(ampelVecino)>0:
                    self.neighbour.append(ampelVecino[0])
                    position =self.model.grid.get_cell_list_contents((self.pos[0]+1, self.pos[1]-2))
                    ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                    self.neighbour.append(ampelVecino[0])
            
#           Abajo Izquierda
            if self.pos[0]-1 >=0 and self.pos[1]-1 >=0 and self.pos[0]-1 <=23 and self.pos[1]-1<=24:
                position =self.model.grid.get_cell_list_contents((self.pos[0]-1, self.pos[1]-1))
                ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                if len(ampelVecino)>0:
                    self.neighbour.append(ampelVecino[0])
                    position =self.model.grid.get_cell_list_contents((self.pos[0]-1, self.pos[1]-2))
                    ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                    self.neighbour.append(ampelVecino[0])
            
#           2 Arriba Derecha
            if self.pos[0]+2 >=0 and self.pos[1]+1 >=0 and self.pos[0]+2 <=23 and self.pos[1]+1<=24:
                position =self.model.grid.get_cell_list_contents((self.pos[0]+2, self.pos[1]+1))
                ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                if len(ampelVecino)>0:
                    self.neighbour.append(ampelVecino[0])
                    position =self.model.grid.get_cell_list_contents((self.pos[0]+2, self.pos[1]+2))
                    ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                    self.neighbour.append(ampelVecino[0])
             
#           2 Arriba Izquierda
            if self.pos[0]-2 >=0 and self.pos[1]+1 >=0 and self.pos[0]-2 <=23 and self.pos[1]+1<=24:
                position =self.model.grid.get_cell_list_contents((self.pos[0]-2, self.pos[1]+1))
                ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                if len(ampelVecino)>0:
                    self.neighbour.append(ampelVecino[0])
                    position =self.model.grid.get_cell_list_contents((self.pos[0]-2, self.pos[1]+2))
                    ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                    self.neighbour.append(ampelVecino[0])
                
#           2 Abajo Derecha
            if self.pos[0]+2 >=0 and self.pos[1]-1 >=0 and self.pos[0]+2 <=23 and self.pos[1]+1<=24:
                position =self.model.grid.get_cell_list_contents((self.pos[0]+2, self.pos[1]-1))
                ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                if len(ampelVecino)>0:
                    self.neighbour.append(ampelVecino[0])
                    position =self.model.grid.get_cell_list_contents((self.pos[0]+2, self.pos[1]-2))
                    ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                    self.neighbour.append(ampelVecino[0])
                
#           2 Abajo Izquierda
            if self.pos[0]-2 >=0 and self.pos[1]-1 >=0 and self.pos[0]-2 <=23 and self.pos[1]-1<=24:
                position =self.model.grid.get_cell_list_contents((self.pos[0]-2, self.pos[1]-1))
                ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                if len(ampelVecino)>0:
                    self.neighbour.append(ampelVecino[0])
                    position =self.model.grid.get_cell_list_contents((self.pos[0]-2, self.pos[1]-2))
                    ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                    self.neighbour.append(ampelVecino[0])

        elif [(self.pos[0], self.pos[1]-1), "Up"] in self.roadMap:
            self.vision[0]=(self.pos[0], self.pos[1]-1)
            self.vision[1]=(self.pos[0], self.pos[1]-2)
            self.vision[2]=(self.pos[0], self.pos[1]-3)
#             Set del hermano
            if self.pos[0]+1 >=0 and self.pos[1] >=0 and self.pos[0]+1 <=23 and self.pos[1]<=24:
                position =self.model.grid.get_cell_list_contents((self.pos[0]+1, self.pos[1]))
                ampelBrother=[obj for obj in position if isinstance(obj,Traffic_Light)]
                if len(ampelBrother)>0:
                    self.brother=ampelBrother[0]
            if self.pos[0]-1 >=0 and self.pos[1] >=0 and self.pos[0]-1 <=23 and self.pos[1]<=24:
                position =self.model.grid.get_cell_list_contents((self.pos[0]-1, self.pos[1]))
                ampelBrother=[obj for obj in position if isinstance(obj,Traffic_Light)]
                if len(ampelBrother)>0:
                    self.brother=ampelBrother[0]
                
#           Arriba Derecha
            if self.pos[0]+1 >=0 and self.pos[1]+1 >=0 and self.pos[0]+1 <=23 and self.pos[1]+1<=24:
                position =self.model.grid.get_cell_list_contents((self.pos[0]+1, self.pos[1]+1))
                ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                if len(ampelVecino)>0:
                    self.neighbour.append(ampelVecino[0])
                    position =self.model.grid.get_cell_list_contents((self.pos[0]+1, self.pos[1]+2))
                    ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                    self.neighbour.append(ampelVecino[0])
                
#            Arriba Izquierda
            if self.pos[0]-1 >=0 and self.pos[1]+1 >=0 and self.pos[0]-1 <=23 and self.pos[1]+1<=24:
                position =self.model.grid.get_cell_list_contents((self.pos[0]-1, self.pos[1]+1))
                ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                if len(ampelVecino)>0:
                    self.neighbour.append(ampelVecino[0])
                    position =self.model.grid.get_cell_list_contents((self.pos[0]-1, self.pos[1]+2))
                    ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                    self.neighbour.append(ampelVecino[0])
             
#           Abajo Derecha
            if self.pos[0]+1 >=0 and self.pos[1]-1 >=0 and self.pos[0]+1 <=23 and self.pos[1]-1<=24:
                position =self.model.grid.get_cell_list_contents((self.pos[0]+1, self.pos[1]-1))
                ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                if len(ampelVecino)>0:
                    self.neighbour.append(ampelVecino[0])
                    position =self.model.grid.get_cell_list_contents((self.pos[0]+1, self.pos[1]-2))
                    ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                    self.neighbour.append(ampelVecino[0])
            
#           Abajo Izquierda
            if self.pos[0]-1 >=0 and self.pos[1]-1 >=0 and self.pos[0]-1 <=23 and self.pos[1]-1<=24:
                position =self.model.grid.get_cell_list_contents((self.pos[0]-1, self.pos[1]-1))
                ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                if len(ampelVecino)>0:
                    self.neighbour.append(ampelVecino[0])
                    position =self.model.grid.get_cell_list_contents((self.pos[0]-1, self.pos[1]-2))
                    ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                    self.neighbour.append(ampelVecino[0])
            
#           2 Arriba Derecha
            if self.pos[0]+2 >=0 and self.pos[1]+1 >=0 and self.pos[0]+2 <=23 and self.pos[1]+1<=24:
                position =self.model.grid.get_cell_list_contents((self.pos[0]+2, self.pos[1]+1))
                ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                if len(ampelVecino)>0:
                    self.neighbour.append(ampelVecino[0])
                    position =self.model.grid.get_cell_list_contents((self.pos[0]+2, self.pos[1]+2))
                    ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                    self.neighbour.append(ampelVecino[0])
             
#           2 Arriba Izquierda
            if self.pos[0]-2 >=0 and self.pos[1]+1 >=0 and self.pos[0]-2 <=23 and self.pos[1]+1<=24:
                position =self.model.grid.get_cell_list_contents((self.pos[0]-2, self.pos[1]+1))
                ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                if len(ampelVecino)>0:
                    self.neighbour.append(ampelVecino[0])
                    position =self.model.grid.get_cell_list_contents((self.pos[0]-2, self.pos[1]+2))
                    ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                    self.neighbour.append(ampelVecino[0])
                
#           2 Abajo Derecha
            if self.pos[0]+2 >=0 and self.pos[1]-1 >=0 and self.pos[0]+2 <=23 and self.pos[1]+1<=24:
                position =self.model.grid.get_cell_list_contents((self.pos[0]+2, self.pos[1]-1))
                ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                if len(ampelVecino)>0:
                    self.neighbour.append(ampelVecino[0])
                    position =self.model.grid.get_cell_list_contents((self.pos[0]+2, self.pos[1]-2))
                    ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                    self.neighbour.append(ampelVecino[0])
                
#           2 Abajo Izquierda
            if self.pos[0]-2 >=0 and self.pos[1]-1 >=0 and self.pos[0]-2 <=23 and self.pos[1]-1<=24:
                position =self.model.grid.get_cell_list_contents((self.pos[0]-2, self.pos[1]-1))
                ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                if len(ampelVecino)>0:
                    self.neighbour.append(ampelVecino[0])
                    position =self.model.grid.get_cell_list_contents((self.pos[0]-2, self.pos[1]-2))
                    ampelVecino=[obj for obj in position if isinstance(obj,Traffic_Light)]
                    self.neighbour.append(ampelVecino[0])

            
    def step(self):
        if self.countStep==0:
            self.setSensor()
            countStep=1
        self.ampelLogic()
        
        """
        self.sema1=[(0,15),(0,16),(0,17)]
        self.cont=0
        "To change the state (green or red) of the traffic light in case you consider the time to change of each traffic light."
        if self.unique_id == "tl_18" or self.unique_id == "tl_42" or self.unique_id == "tl_64" or self.unique_id == "tl_65":
            self.currentStep += 1
            if self.currentStep == 8:
                self.state = "yellow"
            elif self.currentStep == 10:
                self.state = "red"
            elif self.currentStep == 20:
                self.currentStep = 0
                self.state= "green"
                """


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
