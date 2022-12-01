# TC2008B. Sistemas Multiagentes y Gráficas Computacionales
# Python flask server to interact with Unity. Based on the code provided by Sergio Ruiz.
# Octavio Navarro. October 2021

from flask import Flask, request, jsonify
from model import *
from agent import *

# Size of the board:
number_agents = 10
width = 24
height = 25
randomModel = None
currentStep = 0

app = Flask("Traffic example")

# @app.route('/', methods=['POST', 'GET'])

@app.route('/init', methods=['POST', 'GET'])
def initModel():
    global currentStep, randomModel, number_agents

    if request.method == 'POST':
        number_agents = int(request.form.get('NAgents'))
        currentStep = 0

        print(request.form)
        print(number_agents)
        randomModel = RandomModel(number_agents)
        print(f"width :{randomModel.width}")
        print(f"height :{randomModel.height}" )

        return jsonify({"message":"Parameters recieved, model initiated."})

@app.route('/getAgents', methods=['GET'])
def getAgents():
    global randomModel

    if request.method == 'GET':
    #agentPositions = [{"id": str(X.unique_id), "x": x, "y":1, "z":y} for (X, x,y) in carringModel.grid.coord_iter() if isinstance(X, Stevedor)]
        agentPositions = []
        for(N,x, y) in randomModel.grid.coord_iter():
            for i in range(len(N)):
                if isinstance(N[i], Car):
                    agentPositions.append({"id": str(N[i].unique_id), "x": x, "y":1, "z":y})
        
        return jsonify({'positions':agentPositions})

"""
@app.route('/getSemaforos', methods=['GET'])
def getSemaforos():
    global randomModel
    
    if request.method == 'GET':
        carPositions = [{"id": str(a.unique_id), "x": x, "y":1, "z":y} for (a, x, z) in randomModel.grid.coord_iter() if isinstance(a, ObstacleAgent)]

        return jsonify({'positions':carPositions})
"""

@app.route('/update', methods=['GET'])
def updateModel():
    global currentStep, randomModel
    if request.method == 'GET':
        randomModel.step()
        currentStep += 1
        return jsonify({'message':f'Model updated to step {currentStep}.', 'currentStep':currentStep})

if __name__=='__main__':
    app.run(host="localhost", port=8585, debug=True)