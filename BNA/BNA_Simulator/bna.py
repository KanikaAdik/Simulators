import os, re, json, time
from functools import wraps
from flask import Flask, Response, request
from werkzeug.routing import BaseConverter
import socket

app = Flask(__name__)
AUTH_HEADER = "cm9vdDpyb290MTIz"

def get_times(starttime, endtime):
    try:
        times = {}
        startTime = int(round(starttime / 1000))
        endTime   = int(round(endtime / 1000))

        temp = int(round(startTime % 60))
        time_to_add = 60 - temp

        firstTime = startTime + time_to_add
        secondTime = firstTime + 300
        thirdTime = secondTime + 300

        times['startTime'] = starttime
        times['endTime'] = endtime
        times['firstTime'] = firstTime
        times['secondTime'] = secondTime
        times['thirdTime'] = thirdTime
    except Exception as e:
        print ("Error while time manipulations : %s" % str(e))
    return times

def write_json(filename=None,data=None):
    try: 
        with open(filename, 'w') as fp: 
           json.dump(data,fp,indent=4) 
    except Exception as e: 
        print ("Error while writing json file : %s" % str(e))

    return True

def read_json(response_json = None):
    response = None
    try:
        if os.path.exists(response_json):
            try:
                with open(response_json) as json_file:
                    response = json.load(json_file)
            except Exception as e:
                print ("Invalid Json : %s" % response_json) 
                print ("Error in read json: %s " % str(e) )
            fh = open(response_json)
            response = fh.read()
            fh.close()
        else:
            print ("File not found!!!!!!!!!! %s" % response_json)
    except Exception as e:
        print ("Error While reading json file : %s" % str(e))
    return response


def read_special_json(response_json = None):
    response = None
    try:
        if os.path.exists(response_json):
            with open(response_json) as json_file:
                response = json.load(json_file)
        else:
            print ("File not found!!!!!!!!!! %s" % response_json)
    except Exception as e:
        print ("Error While reading json file : %s" % str(e))
    return response


def fetch_response(request_path,ip=None,request_url=None):
    startDate = endDate = None
    try:
        output_dir = os.path.join(os.getcwd(),"outputs")
        if request_path == "/rest/login":
            response_json = os.path.join(output_dir, "login.json")
 
        elif "granularity" not in request_url:

           if os.path.basename(request_path) in ['fcswitches','accessgateways',"fcfabrics"]:
               dir_path = os.path.dirname(request_path).strip("/")
               filname = "%s_f" % os.path.basename(request_path)
               response_json = os.path.join(output_dir,dir_path,filname)
           else:
               request_path = request_path.strip("/")
               response_json = os.path.join(output_dir,request_path.split("?")[0])
        
        elif "granularity" in request_url:
            filepath = request_path.strip("/")
            response_json = os.path.join(output_dir,filepath.split("?")[0])

            date_args = request_url.split("&")
            for item in date_args:
                if "startdate" in item:
                     startDate = item.split("=")[1]
                     startDate = startDate.strip("]")
                     startDate = startDate.strip("[")
                elif "enddate" in item:
                     endDate = item.split("=")[1]
                     endDate = endDate.strip("]")
                     endDate = endDate.strip("[") 

        else:
           print ("Invalid Request Obtained %s" % request_path)
    
        if startDate and endDate:
           response = get_modified_response(response_json, int(startDate) , int(endDate))
        else:
            response = read_json(response_json)

        if not response:
            print (request_path, "!!!!!!!!!!!!!!!!!! failed!!!!!!!!!!!!!!!!")
    
    except Exception as e:
         print ("Error : %s" % str(e))
        
    return response 

def get_modified_response(fileName, startDate , endDate):
    times = {}
    response = None
    try:
        times = get_times(startDate, endDate) 
        temp_resp = read_json(fileName)

        temp_op_file = os.path.join(os.getcwd(),"output.json") 
        write_json(temp_op_file, temp_resp)
 
        cmd = "sed -i 's/11111111/%s/g' %s" % (times["startTime"],temp_op_file)
        os.system(cmd)
 
        cmd = "sed -i 's/22222222/%s/g' %s" % (times['endTime'],temp_op_file)
        os.system(cmd)

        cmd = "sed -i 's/33333333/%s/g' %s" % (times['firstTime'],temp_op_file)
        os.system(cmd)

        cmd = "sed -i 's/44444444/%s/g' %s" % (times['secondTime'],temp_op_file)
        os.system(cmd)

        cmd = "sed -i 's/55555555/%s/g' %s" % (times['thirdTime'],temp_op_file)
        os.system(cmd)

        '''
        response = temp_resp.replace("11111111", times['startTime'])
        response = response.replace("22222222",times['endTime'])
        response = response.replace("33333333",times['firstTime'] )
        response = response.replace("44444444", times['secondTime'])
        response = response.replace("55555555",times['thirdTime'])
        '''
        response = read_special_json(temp_op_file)
        #response = read_json(temp_op_file)
       
    except Exception as e:
        print ("Error while modifying response : %s" % str(e))

    return response

def check_auth(username, password):
    print (username, password)
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'root' and password == 'root123'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            print ("=====================================")
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@app.route('/', methods=['GET', 'POST'], defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST'])
@app.route('/')
def all(path):
    print ("##########", request.path, request.url)
    ip = (request.url).split('/')[2].replace('.','').split(':')[0]
    if request.path == "/rest/logout":
        return ('',200)
    response_json = fetch_response(request.path,ip,request.url) 
    resp = Response(response_json, mimetype='application/json')
    resp.headers['WStoken'] = AUTH_HEADER
    return resp
    #return Response(response_json, mimetype='application/json')
 

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=80)


