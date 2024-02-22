import os, re, json, time
from functools import wraps
from flask import Flask, Response, request
from werkzeug.routing import BaseConverter

app = Flask(__name__)

response_dir = os.path.join(os.getcwd(), "responseJson")

def fetch_response(url, request_data, ip):
    response = None

    try:
        folder_name = url.split('performance/')[1].replace('/', '_')
    except:
        if url == "/univmax/restapi/system/version" :
            folder_name = os.path.join("system", "version")
            response_json = os.path.join(response_dir, folder_name, "output.json")
            response = read_json(response_json)
            if not response:
                print url, request_data, "!!!!!!!!!!!!!!!!!! failed!!!!!!!!!!!!!!!!"
            return response
    try:
        request_data = json.loads(request_data)
    except:
        response_json = os.path.join(response_dir, folder_name, "output.json")
        response = read_json(response_json)
        if not response:
            print url, request_data, "!!!!!!!!!!!!!!!!!! failed!!!!!!!!!!!!!!!!"
        response = update_response(response, {})
        response = response.replace("000296800969",str(ip).zfill(12))
        return response

    if request_data.has_key('symmetrixId'):
        #folder_name = os.path.join(folder_name, request_data['symmetrixId'])
        folder_name = os.path.join(folder_name, "000296800969")

    if request_data.has_key('directorId'):
        folder_name = os.path.join(folder_name, request_data['directorId'])

    if request_data.has_key('portGroupId'):
        folder_name = os.path.join(folder_name, request_data['portGroupId'])

    if request_data.has_key('deviceGroupId'):
        folder_name = os.path.join(folder_name, request_data['deviceGroupId'])

    if request_data.has_key('portId'):
        folder_name = os.path.join(folder_name, request_data['portId'])

    if request_data.has_key('diskGroupId'):
        folder_name = os.path.join(folder_name, request_data['diskGroupId'])

    if request_data.has_key('storageGroupId'):
        folder_name = os.path.join(folder_name, request_data['storageGroupId'])

    if request_data.has_key('poolId'):
        folder_name = os.path.join(folder_name, request_data['poolId'])

    response_json = os.path.join(response_dir, folder_name, "output.json")
    response = read_json(response_json)
    if not response:
        print url, request_data

    response = update_response(response, request_data)

    response = response.replace("000296800969",str(ip).zfill(12))
    return response

def update_response(response, request_data):

    # allign time
    interval = 5
    b        = 60000 * interval
    end_time = int(round(time.time() * 1000))
    new_end_time = end_time - (end_time % b)

    try:
        #response = re.sub('.*?lastAvailableDate.*?:.*?(\d+)','"lastAvailableDate" : %s' % int(round(time.time() * 1000)), response)
        response = re.sub('.*?lastAvailableDate.*?:.*?(\d+)','"lastAvailableDate" : %s' % new_end_time, response)
    except:
        print response,"re sub failed"
    try:
        response = re.sub('.*?expirationTime.*?:.*?(\d+)','"expirationTime" : %s' % new_end_time, response)
    except:
        print response,"re sub failed"


    try:
        response = json.loads(response)
    except:
        print "Error loading JSON response!!, ", response

    try:
       startDate = request_data['startDate']
       endDate   = request_data['endDate']
       response['resultList']['result'] = update_result_list(response['resultList']['result'], startDate, endDate)
    except Exception as e:
       import traceback, sys
       exc_info = sys.exc_info()
       traceback.print_exception(*exc_info)

       print "startDate, endDate not found", response, request_data
       pass

    return json.dumps(response, indent=4)

def update_result_list(results, startDate, endDate):
    startDate = int(startDate)
    endDate   = int(endDate)
    timestamps = get_all_timestamps(startDate, endDate, 5)
    count = 0
    output = []
    for result in results:
        try:
           result['timestamp'] = timestamps[count]
           count = count + 1
        except:
           pass
        output.append(result)
    return output

def get_all_timestamps(startDate, endDate, interval):
    timestamps = [startDate]
    currentTime = startDate
    while currentTime < endDate:
        currentTime = currentTime + (60000*interval)
        timestamps.append(currentTime)
    #timestamps.append(endDate)
    return timestamps

def read_json(response_json):
    response = None
    if os.path.exists(response_json):
        fh = open(response_json)
        response = fh.read()
        fh.close()
    else:
        print "File not found!!!!!!!!!! %s" % response_json
    return response

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'Admin@123'

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
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@app.route('/', methods=['GET', 'POST'], defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST'])
@requires_auth
def all(path):
    #print "##########", request.path, request.url
    ip = (request.url).split('/')[2].replace('.','').split(':')[0]
    response_json = fetch_response(request.path, request.data, ip)
    return Response(response_json, mimetype='application/json')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8443, ssl_context='adhoc')
