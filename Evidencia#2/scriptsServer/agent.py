import random
from mesa import Agent

class Car(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID 
        direction: Randomly chosen direction chosen from one of eight directions
    """
    def __init__(self, unique_id, model,des):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)
        self.destination = des
        self.lastDirection = "Left"


    def move(self):
        """ 
        Determines if the agent can move in the direction that was chosen
        """ 
        x0,y0 = self.pos
        xf,yf = self.destination
        position =self.model.grid.get_cell_list_contents([self.pos])
        direccionRoad=[obj for obj in position if isinstance(obj,Road)]
        goOrStop=[obj for obj in position if isinstance(obj,Traffic_Light)]
        if len(direccionRoad)>0:
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
        else:
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
