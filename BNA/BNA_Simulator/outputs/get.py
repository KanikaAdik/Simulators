import os,re,json
import subprocess

#f=os.path.join(os.sep,"root","requests")
f=os.path.join(os.getcwd(),"requests")
fh=open(f)
lines=fh.readlines()
fh.close()
for line in  lines:
    reqres=  line.split(" ")[3:]
    try:
        request = reqres[0].split("[")[1].split("]")[0]
        reqres[4] = " ".join(reqres[4:])
        response =  reqres[4].split("[",1)[1].rsplit("]",1)[0]
    except:
        request = reqres[1].split("[")[1].split("]")[0]
        response =  reqres[5].split("[",1)[1].rsplit("]",1)[0]
   
    #response =  reqres[4].split("[",1)[1].rsplit("]",1)[0]
    #path = os.path.join(os.sep,"root")
    path = os.getcwd()
    print request.split("/")
    for each in request.split("/")[3:]:
         if '?' in  each:
              if each in ['fcfabrics','fcswitches','accessgateways']:
                   each = each+"_f"
              filename = each.split("?")[0]
              flnm = os.path.join(path,filename)
              fh = open(flnm, "w")
              #response = json.loads(response)
              #fh.write(json.dumps(response, indent=4))
              fh.write(response)
              fh.close()
         elif each  == request.split("/")[3:][-1]:
              if each in ['fcfabrics','fcswitches','accessgateways']:
                   each = each+"_f"
              flnm = os.path.join(path,each)
              fh = open(flnm, "w")
              fh.write(response)
              fh.close()
         else:
              path = os.path.join(path,each)
              if not os.path.exists(path):
                  os.mkdir(path)
              elif os.path.isfile(path):
                  os.mkdir(path)
                  
print "DONE!"
