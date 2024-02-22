import json,os,shutil,sys

global FAB_ID , SWITCH_COUNT
FAB_ID       = 200
SWITCH_COUNT = 1

def write_json(filename=None,data=None):
    try:
        with open(filename, 'w') as fp:
           json.dump(data,fp,indent=4)
    except Exception as e:
        print "Error while writing json file : %s" % str(e)

    return True

def read_special_json(response_json = None):
    response = None
    try:
        if os.path.exists(response_json):
            with open(response_json) as json_file:
                response = json.load(json_file)
        else:
            print "File not found!!!!!!!!!! %s" % response_json
    except Exception as e:
        print "Error While reading json file : %s" % str(e)
    return response

def write_file(filename,dump_data):
    file = open(filename,'w')
    file.write(json.dumps(dump_data))
    file.close()

def copy_dir(dir_name,output_dir_name):
    try:
        if os.path.exists(output_dir_name):
            print "Output dir already exists, exiting..."
            sys.exit(0)
        else:
            cmd = "cp -r %s %s" % (dir_name,output_dir_name) 
            os.system(cmd) 
        
    except Exception as e:
        print "Error while copying directory : %s" % str(e) 

#Fun for creating duplicate data's for timeseriesutilpercentage and timeseriestraffic
def create_duplicate_data(filename,replace_key):
    data = read_special_json(filename)
    copy_data = data.copy()
    new_data = data.copy()

    item1 = None
    try:
        for item in copy_data['performanceDatas']:
            item1 = None
            item1 = item.copy()
            if item.has_key("targetKey") and "00:05:33:B7:75:D5" in item["targetKey"]:
                new_key = item1["targetKey"].replace("00:05:33:B7:75:D5", replace_key)

                item1["targetKey"]=new_key
                new_data['performanceDatas'].append(item1)

        write_file(filename,new_data) 
    except Exception as e:
        print "Error while modifying file : %s" % str(e)

    return True

def keep_backup_file(filename):
    try:
        dest_file = os.path.join("%s.bak" % filename) 
        shutil.copy(filename, dest_file)
    except Exception as e:
        print "Error while creting backup file : %s" % str(e)

def create_cpu_mem_data(filename,wwn_key):
    data = read_special_json(filename)
    copy_data = data.copy()
    new_data = data.copy()
    item1 = None
    try:
        for item in copy_data['performanceDatas']:
            if item.has_key('targetKey') and item['targetKey'] == '10:00:00:05:33:B7:75:D5':
                temp_dict = item.copy()
                break; 
        temp_dict['targetKey'] = wwn_key   
        new_data['performanceDatas'].append(temp_dict)
        write_file(filename,new_data) 
    except Exception as e:
        print "Error while modifying file : %s" % str(e)

def modify_fabrics_file(filename,data,wwn,replace_wwn):
    global FAB_ID 
    try:
        fab_name = "Fab_5100-10:00:%s" % replace_wwn
        new_data = data.copy()   
        dump_data = new_data['fcfabrics'].copy()  
        dump_data['key'] = wwn
        dump_data['seedSwitchWwn'] = wwn
        dump_data['name'] = fab_name
        dump_data['principalSwitchWwn'] = wwn
        dump_data['virtualFabricId'] = FAB_ID 

        FAB_ID += 1

        final_data = read_special_json(filename) 
        temp_data = final_data.copy()
        temp_data["fcFabrics"].append(dump_data) 
        
        write_file(filename,temp_data)
    except Exception as e:
        
        print "Error while fabrics modifying file : %s" % str(e)
    
def modify_rec_fswitches(filename,wwn,replace_wwn):
    global SWITCH_COUNT 
    try:
        data = read_special_json(filename)
        new_data = data.copy()
        dump_data = new_data['fcSwitches'][0].copy()
       
        dump_data['key'] = wwn
        dump_data['name'] = "Simulator_SW_%s" % SWITCH_COUNT
        dump_data['wwn'] = wwn
        dump_data['virtualFabricId'] = FAB_ID

        SWITCH_COUNT += 1

        final_data = read_special_json(filename)
        temp_data = final_data.copy()
        temp_data['fcSwitches'][0].update(dump_data)

        write_file(filename,temp_data)
    except Exception as e:
        print "Error while fcswitches modifying file : %s" % str(e)


def modify_ag_enddevices(filename,wwn,replace_wwn):
    try:
        data = read_special_json(filename)
        copy_data = data.copy()
        new_data = data.copy()

        for item in copy_data["endDevices"]:
            item1 = None
            item1 = item.copy()
            if item.has_key("fabricWwn") and "00:05:33:B7:75:D5" in item["fabricWwn"]:
                new_key = item1["fabricWwn"].replace("00:05:33:B7:75:D5", replace_wwn)
                item1["fabricWwn"]=new_key
                new_data['endDevices'].append(item1)

        write_file(filename,new_data) 
 
    except Exception as e:
        print "Error while endevices modifying file : %s" % str(e)


def modify_agconnections(filename,data,wwn,replace_wwn):
    try:
        dump_data = data.copy()
        new_data = read_special_json(filename)

        dump_data['destinationSwitchWwn'] = wwn
        dest_wwn = "20:17:%s" % replace_wwn
        dump_data['destinationPortWwn'] = dest_wwn
        key = dump_data['key'] 
        dump_key = key.replace('00:05:33:B7:75:D5',replace_wwn)
        dump_data['key'] = dump_key
   
        new_data['agConnections'].append(dump_data)
        write_file(filename,new_data)

    except Exception as e:
        print "Error while agconnections modifying file : %s" % str(e)

def modify_ag_fcports(filename,wwn,replace_wwn):
    try: 
        data = read_special_json(filename)
        copy_data = data.copy()
        new_data = data.copy()
   
        for item in copy_data["fcPorts"]:
            item1 = None
            item1 = item.copy()
            if item.has_key("remoteNodeWwn") and "00:05:33:B7:75:D5" in item["remoteNodeWwn"]:
                 new_key = item1["remoteNodeWwn"].replace("00:05:33:B7:75:D5", replace_wwn)
                 item1["remoteNodeWwn"]=new_key
                 new_data['fcPorts'].append(item1)

            elif item.has_key("remotePortWwn") and "00:05:33:B7:75:D5" in item["remotePortWwn"]:
                 new_key = item1["remotePortWwn"].replace("00:05:33:B7:75:D5", replace_wwn)
                 item1["remotePortWwn"]=new_key
                 new_data['fcPorts'].append(item1)

        write_file(filename,new_data)

    except Exception as e:
        print "Error while fcswitches modifying file : %s" % str(e)


try:
    #Copy resr_outputs dir as rest
    src_dir = os.path.join(os.getcwd(),"rest_outputs")
    dest_dir = os.path.join(os.getcwd(),"rest") 
    copy_dir(src_dir,dest_dir)
    print "Directory copyied successfully"

    temp_ops = os.path.join(os.getcwd(),"temp_ops.json")
    temp_ops_dict = read_special_json(temp_ops)

    wwn_list_file = os.path.join(os.getcwd(),"wwn_list.json")
    wwn_list = read_special_json(wwn_list_file)
    rest_all_dir = os.path.join(os.getcwd(),"rest","resourcegroups","All")

    for wwn in wwn_list:
        #get the replace wwn 
        wwn_temp = wwn.split(":")
        del wwn_temp[:2]
        replace_wwn = ":".join(wwn_temp)
    
        #modify timeseriesutilpercentage file
        timeseriesutilpercentage = os.path.join(rest_all_dir,"timeseriesutilpercentage")
        keep_backup_file(timeseriesutilpercentage) 
        create_duplicate_data(timeseriesutilpercentage,replace_wwn) 
      
        #Modify timeseriestraffic
        timeseriestraffic = os.path.join(rest_all_dir,"timeseriestraffic")
        keep_backup_file(timeseriestraffic)
        create_duplicate_data(timeseriestraffic,replace_wwn)

        #Modidy timeseriescpuutilpercentage and timeseriesmemoryutilpercentage
        timeseriescpuutilpercentage = os.path.join(rest_all_dir,"timeseriescpuutilpercentage")
        keep_backup_file(timeseriescpuutilpercentage)
        create_cpu_mem_data(timeseriescpuutilpercentage,wwn)

        timeseriesmemoryutilpercentage = os.path.join(rest_all_dir,"timeseriesmemoryutilpercentage") 
        keep_backup_file(timeseriesmemoryutilpercentage) 
        create_cpu_mem_data(timeseriesmemoryutilpercentage,wwn) 

        #Modify fcfabrics_f file 
        fcfabrics_f = os.path.join(rest_all_dir,"fcfabrics_f")
        keep_backup_file(fcfabrics_f)
        fcfabrics = temp_ops_dict['fcfabrics'].copy()
        modify_fabrics_file(fcfabrics_f,temp_ops_dict,wwn,replace_wwn) 

        #Copy fcswitchs/<wwn_dir> to wwn dir
        wwn_dir = os.path.join(rest_all_dir,"fcswitches","10:00:00:05:33:B7:75:D5")
        dest_dir = os.path.join(rest_all_dir,"fcswitches",wwn) 
        copy_dir(wwn_dir,dest_dir) 
    
        new_fcswitchs_dir = os.path.join(rest_all_dir,"fcswitches",wwn)
        cmd = "grep -rl '00:05:33:B7:75:D5' %s | xargs sed -i 's/00:05:33:B7:75:D5/%s/g'" % (new_fcswitchs_dir,replace_wwn)    
        os.system(cmd) 


        #Copy fcfabrics/<wwn_dir> to wwn dir
        wwn_dir = os.path.join(rest_all_dir,"fcfabrics","10:00:00:05:33:B7:75:D5")
        dest_dir = os.path.join(rest_all_dir,"fcfabrics",wwn)
        copy_dir(wwn_dir,dest_dir)
   
        #Rename dir present in fcfabrics/<wwn_dir>/fcswitches/<wwm>
        rec_dir = os.path.join(dest_dir,"fcswitches","10:00:00:05:33:B7:75:D5")
        move_dir = os.path.join(dest_dir,"fcswitches",wwn) 
        os.rename(rec_dir,move_dir) 
    

        #Change rec fcswitches_f file
        fcswitches = os.path.join(dest_dir, "fcswitches_f")
        modify_rec_fswitches(fcswitches, wwn ,replace_wwn)
        cmd = "grep -rl '00:05:33:B7:75:D5' %s | xargs sed -i 's/00:05:33:B7:75:D5/%s/g'" % (dest_dir,replace_wwn)
        os.system(cmd)

        #Changes agconnections files
        enddevies = os.path.join(rest_all_dir,"accessgateways","10:00:00:05:33:9E:66:0C","enddevices")
        modify_ag_enddevices(enddevies,wwn,replace_wwn) 

        fcports = os.path.join(rest_all_dir,"accessgateways","10:00:00:05:33:9E:66:0C","fcports")
        modify_ag_fcports(fcports,wwn,replace_wwn)         

        #Modify agconnections file
        agconnections = os.path.join(rest_all_dir,"agconnections")
        agcon_dict = temp_ops_dict['agConnections'].copy()
        modify_agconnections(agconnections,agcon_dict,wwn,replace_wwn)

except Exception as e:
    print "Error : %s\n Exiting..." % str(e)
    sys.exit(0)
