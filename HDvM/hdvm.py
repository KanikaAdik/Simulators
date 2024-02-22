from functools import wraps
from flask import request, Response, Flask, url_for
from werkzeug.routing import BaseConverter
import os,re, arrow

app =Flask(__name__)

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'secret'

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

def find_target(req):
    target = None
    cmds = ['ArrayGroup','JournalPool','LDEV','WorldWideName','Port','StorageArray','ServerInfo']
    for cmd in cmds:
        if cmd in req:
            target = cmd
            break
    if not target:
        print ("didnot find cmd in ::", req)
    return target

def fetch_response(url, request_data):
    response = None
    target = find_target(request.data)
    f = os.path.join(os.sep,os.getcwd(),"dumps",target)
    fh = open (f, 'r')
    response = fh.read()
    fh.close()
    return response
 
@app.route('/', methods=['GET', 'POST'], defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST'])
@requires_auth
def all(path):
    #ip = (request.url).split('/')[2].replace('.','').split(':')[0]
    response_json = fetch_response(request.path, request.data) 
    return Response(response_json, mimetype='text/xml')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port='2443', ssl_context='adhoc')

