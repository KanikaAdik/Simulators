import  os,requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
#r = requests.post("https://192.168.20.27:2443/service/StorageManager")
URL = "https://192.168.20.27:2443/service/StorageManager"
 
f = os.path.join(os.sep,"data","hdvm","cmds")
fh = open(f, 'r')
cmds = fh.readlines()
fh.close()

headers = {'Authorization': 'Basic c3lzdGVtOm1hbmFnZXI=', 
           'Content-Type':'text/xml'}

filenames = ['ArrayGroup','JournalPool','LDEV','WorldWideName','Port','StorageArray','ServerInfo']

for cmd in  cmds:
    for name in filenames:
        if name in cmd:
            filename = name
            break
    data = cmd
    r = requests.post(url = URL,headers = headers, data = data, verify=False)
    response =  r.content
    f = os.path.join(os.sep,"data","hdvm","dumps",name)
    fh = open(f, "w")
    fh.write(response)
