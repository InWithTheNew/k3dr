import random
import json
import subprocess
import socket
import string
from .HelmRelease import HelmRelease

class K3dConfig:

  # def __init__(self, name):
  #   self.httpPort = random.randint(1000,62555)
  #   self.httpsPort = self.httpPort+1
  #   self.apiPort = self.httpPort+2
  #   self.clusterName = name
  #   self.masterAgents = 1
  #   self.workerAgents = 1

  def __init__(self, masterAgents = 1, workerAgents = 1, ingressEnabled = "false", uid = ""):
    self.httpPort = random.randint(1000,62555)
    self.httpsPort = self.httpPort+1
    self.apiPort = self.httpPort+2
    self.masterAgents = masterAgents
    self.workerAgents = workerAgents
    self.ingressEnabled = ingressEnabled
    if uid == "":
      self.uid = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    else:
      self.uid = uid.strip("k3d-")
    
    
  def create(self):
    hostname = socket.gethostname()
    # try:
    subprocess.run(["k3d", 
                  "cluster", 
                  "create", 
                  f"{self.uid}", 
                  "--port", f"{self.httpPort}:80@loadbalancer", 
                  "--port", f"{self.httpsPort}:443@loadbalancer", 
                  "--api-port", f"{self.apiPort}", 
                  "--servers", f"{self.masterAgents}", 
                  "--agents", f"{self.workerAgents}", 
                  "--k3s-arg", f"\"--tls-san={hostname}\"@loadbalancer"
                  ])
    if self.ingressEnabled == "true":
      q = HelmRelease(f"{self.uid}", "nginx-ingress", "default", "https://helm.nginx.com/stable")
      q.install()
    self.kubeCredentials = self.get_credentials(self.uid, hostname)
    data = {}
    data['instanceName'] = self.uid
    data['ingress'] = self.ingressEnabled
    if self.ingressEnabled == "true":
      data['ingressAddress'] = f"https://{hostname}:{self.httpsPort}"
    data['kubeConnectionString'] = self.kubeCredentials
    json_data = json.dumps(data)
    return json_data
    # except:
    #   print("An error has occurred!")

  def get_credentials(self, name, hostname):
    try:
      getcreds = subprocess.run(args = [
        "sh",
        "-c",
        # f"k3d kubeconfig print {name} | sed \"s/0.0.0.0/{hostname}/g\""
        f"kubectl config view --minify --flatten -o json | sed \"s/0.0.0.0/{hostname}/g\""
      ],     
        capture_output = True,
        text = True 
      )
      result = json.loads(getcreds.stdout)
      return result
    except:
      print("An error has occurred when getting credentials!")

  def delete(self):
      hostname = socket.gethostname()
      try:
        deletek3d = subprocess.run(args = [
          "k3d", 
          "cluster", 
          "delete", 
          f"{self.uid}"
        ],     
          capture_output = True,
          text = True )
        if "No clusters found" in deletek3d.stdout:
          response = "No clusters found"
        else:
          response = f"{self.uid} has been deleted from {hostname}"
        return response
      except:
        print("An error has occurred!")