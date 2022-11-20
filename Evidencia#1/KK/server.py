from flask import Flask, request, jsonify
from RandomAgents import *

width = 10 
height = 10
X = 10 #numero de agentes.
p = 25 #porcentaje de cajas respecto al width y height
e = 0  #tiempo de ejecución pero no afecta en nada. 

app = Flask("Equipo#1")

@app.route('/init', methods=['POST', 'GET'])
def initModel():
    global width, height, X, p, e, carringModel

    if request.method == 'POST':
        width = int(request.form.get('width'))
        height = int(request.form.get('height'))
        X = int(request.form.get('NAgents'))
        p = float(request.form.get('XBox'))
        e = 0

        print(request.form)
        print(width, height, X, p)
        carringModel = CarringModel(width, height, X, p)

        return jsonify({"message":"Parameters recieved, model initiated."})

@app.route('/getAgents', methods=['GET'])
def getAgents():
    global carringModel

    if request.method == 'GET':
        agentPositions = [{"id": str(X.unique_id), "x": x, "y":1, "z":z} for (X, x, z) in carringModel.grid.coord_iter() if isinstance(X, Stevedor)]

        return jsonify({'positions':agentPositions})

#Falta la app route de las cajas
#
#
#
#

@app.route('/update', methods=['GET'])
def updateModel():
    global currentStep, carringModel
    if request.method == 'GET':
        carringModel.step()
        currentStep += 1
        return jsonify({'message':f'Model updated to step {currentStep}.', 'currentStep':currentStep})

if __name__=='__main__':
    app.run(host="localhost", port=8585, debug=True)

