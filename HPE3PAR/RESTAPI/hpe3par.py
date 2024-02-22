import os, json
from flask import Flask

app = Flask(__name__)

@app.route("/api")
def api_response():
  path = os.path.join(os.getcwd(),"api","v1","api")
  fh = open(path,"r")
  response = fh.read()
  fh.close
  return response
 
@app.route("/api/v1/<command>")
def get_response(command):
  #path = os.path.join(os.getcwd(),  sep, "root", "HPE3PAR","RESTAPI","api","v1",command)
  path = os.path.join(os.getcwd(),"api","v1",command)
  fh = open(path,"r")
  response = fh.read()
  fh.close
  return response

if __name__ == "__main__":
  app.run("0.0.0.0","80")


"""

https://10.250.138.128:8080/api
https://10.250.138.128:8080/api/v1/cpgs
https://10.250.138.128:8080/api/v1/capacity
https://10.250.138.128:8080/api/v1/cpgs
https://10.250.138.128:8080/api/v1/hosts
https://10.250.138.128:8080/api/v1/hostsets
https://10.250.138.128:8080/api/v1/ports
https://10.250.138.128:8080/api/v1/qos
https://10.250.138.128:8080/api/v1/roles
https://10.250.138.128:8080/api/v1/system
https://10.250.138.128:8080/api/v1/tasks
https://10.250.138.128:8080/api/v1/users
https://10.250.138.128:8080/api/v1/vluns
https://10.250.138.128:8080/api/v1/volumes
https://10.250.138.128:8080/api/v1/volumesets
https://10.250.138.128:8080/api/v1/wsapiconfiguration

"""
