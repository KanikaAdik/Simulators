import glob, os, json

logs = glob.glob('probe.log*')

def dump_to_file(request, req_type, param, output):

    #print "-" * 120
    #print request
    #if req_type == 'POST':
    #    print param
    #print output

    folder_name = os.path.join(os.getcwd(), "responseJson", request.split('performance/')[1].replace('/','_'))
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    if req_type == 'POST':
        param = json.loads(param)
        if param.has_key('symmetrixId'):
            folder_name = os.path.join(folder_name, param['symmetrixId'])
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
            #del param['symmetrixId']

        if param.has_key('directorId'):
            folder_name = os.path.join(folder_name, param['directorId'])
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
            #del param['directorId']

        if param.has_key('portGroupId'):
            folder_name = os.path.join(folder_name, param['portGroupId'])
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
            #del param['portGroupId']

        if param.has_key('deviceGroupId'):
            folder_name = os.path.join(folder_name, param['deviceGroupId'])
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
            #del param['deviceGroupId']

        if param.has_key('portId'):
            folder_name = os.path.join(folder_name, param['portId'])
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
            #del param['portId']

        if param.has_key('diskGroupId'):
            folder_name = os.path.join(folder_name, param['diskGroupId'])
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
            #del param['diskGroupId']

        if param.has_key('storageGroupId'):
            folder_name = os.path.join(folder_name, param['storageGroupId'])
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
            #del param['storageGroupId']

        if param.has_key('poolId'):
            folder_name = os.path.join(folder_name, param['poolId'])
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
            #del param['poolId']

        """
        if param.has_key('metrics'):
            del param['metrics']

        if param.has_key('startDate'):
            del param['startDate']

        if param.has_key('dataFormat'):
            del param['dataFormat']

        if param.has_key('endDate'):
            del param['endDate']
        """

    output_file = os.path.join(folder_name, "output.json")
    param_file  = os.path.join(folder_name, "param.json")

    if not os.path.exists(output_file):
        fh = open(output_file, 'w')
        output = json.loads(output)
        fh.write(json.dumps(output, indent=4))
        fh.close()

    if not os.path.exists(param_file):
        fh = open(param_file, 'w')
        fh.write(json.dumps(param, indent=4))
        fh.close()

    #print "-" * 120


for log in logs:
    fh = open(log)
    #log_text = fh.readlines()
    log_text = fh.read().replace('\n','')
    fh.close()

    log_text = log_text.split('2017-05-05')

    param = request = output = None
    for line in log_text:
        if 'Json request body for V2' in line:
            param = line.split('Json request body for V2: ')[1]
        if 'https' in line:
            request  = line.split('request:')[1].split(' ')
            req_type = request[1]
            request  = request[2]
        if 'Json response output' in line:
            output = line.split('Json response output: ')[1]
            dump_to_file(request, req_type, param, output)
