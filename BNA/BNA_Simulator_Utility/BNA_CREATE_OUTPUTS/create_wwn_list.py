import os,sys,json

START_WWN = '10:00:00:05:33:B7:75:D7'
No_WWNS = 2

filename = os.path.join(os.getcwd(),'wwn_list.json')

def write_json(filename=None,data=None):
    try:
        with open(filename, 'w') as fp:
           json.dump(data,fp,indent=4)
    except Exception as e:
        print "Error while writing json file : %s" % str(e)

    return True

def pairwise(it):
        it = iter(it)
        while True:
            yield next(it), next(it)

def get_wwn(wwn):
        wwns = {}
        for i in range(No_WWNS):
            #wwn = format(i, 'X').zfill(16)
            w=[]
            for a, b in pairwise(wwn):
                byte = "%s%s"%(a,b)
                w.append(byte)
            wwns.update({i:w})
            wwn = '{:X}'.format(int(wwn, 16)+1)
        replace_wwn = []
        for each in wwns.values():
            replace_wwn.append((":").join(each))
        return replace_wwn

start_wwn = "".join(START_WWN.split(":"))
wwn_list = get_wwn(start_wwn)
write_json(filename,wwn_list) 

