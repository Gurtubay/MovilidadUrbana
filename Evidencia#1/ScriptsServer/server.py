from flask import Flask, request, jsonify
from RandomAgents import *

width = 10 
height = 10
X = 5 #numero de agentes.
p = 10 #porcentaje de cajas respecto al width y height
e = 0  #tiempo de ejecución pero no afecta en nada. 
currentStep = 0

app = Flask("Equipo#1")

@app.route('/init', methods=['POST', 'GET'])
def initModel():
    global width, height, X, p, e, carringModel, currentStep 

    if request.method == 'POST':
        width = int(request.form.get('width'))
        height = int(request.form.get('height'))
        X = int(request.form.get('NAgents'))
        p = float(request.form.get('XBox'))
        e = 0
        currentStep = 0

        print(request.form)
        print(width, height, X, p)
        carringModel = CarringModel(width, height, X, p, e)

        return jsonify({"message":"Parameters recieved, model initiated."})

@app.route('/getAgents', methods=['GET'])
def getAgents():
    global carringModel

    if request.method == 'GET':
    #agentPositions = [{"id": str(X.unique_id), "x": x, "y":1, "z":y} for (X, x,y) in carringModel.grid.coord_iter() if isinstance(X, Stevedor)]
        agentPositions = []
        for(X,x, y) in carringModel.grid.coord_iter():
            for i in range(len(X)):
                if isinstance(X[i], Stevedor):
                    agentPositions.append({"id": str(X[i].unique_id), "x": x, "y":1, "z":y})

        return jsonify({'positions':agentPositions})
#duda
@app.route('/getBoxes', methods=['GET'])
def getBoxes():
    global carringModel

    if request.method == 'GET':
        #boxPositions = [{"id": str(d.unique_id), "x": x, "y":1, "z":y} for (d, x, y) in carringModel.grid.coord_iter() if isinstance(d, Box)]
        boxPositions = []
        for(d,x, y) in carringModel.grid.coord_iter():

            for i in range(len(d)):
                if isinstance(d[i], Box):
                    boxPositions.append({"id": str(d[i].unique_id), "x": x, "y":d[i].altura, "z":y})
        return jsonify({'positions':boxPositions})

@app.route('/update', methods=['GET'])
def updateModel():
    global currentStep, carringModel
    if request.method == 'GET':
        carringModel.step()
        currentStep += 1
        if carringModel.renacimiento:
            return jsonify({'message':f'666'})
        return jsonify({'message':f'Model updated to step {currentStep}.', 'currentStep':currentStep})
    

if __name__=='__main__':
    app.run(host="localhost", port=8585, debug=True)

