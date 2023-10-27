from models.K3dConfig import K3dConfig
from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def welcome():
    return "You've reached the K3D creator index. use /create to create a cluster and /delete to delete a cluster"

@app.route('/v1/k3dr', methods=['POST', 'DELETE'])
def k3d_cluster():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        if request.method == "POST":
            json = request.get_json()
            p = K3dConfig(json["masterAgentCount"], json["workerAgentCount"], json["ingressEnabled"])
            result = p.create()
            return result
        elif request.method == "DELETE":
            json = request.get_json()
            p = K3dConfig(uid=json["uid"])
            result = p.delete()
            return result
    else:
        return 'Content-Type not supported!'
    
if __name__ == "__main__":    
    app.run(debug=True)