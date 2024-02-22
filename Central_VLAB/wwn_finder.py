import os, sys , re, glob


class wwn_finder:
    PORT_REGEX = '.*?(([0-9A-Fa-f]{2}[:-]){7}[0-9A-Fa-f]{2}).*?'
    PORTS = []
    def __init__(self,probedir):
        self.work_dir = os.path.join(os.getcwd(),probedir)
        self.log_file = os.path.join(os.getcwd(),"serach_replace.log")
        
    def write_to_file(self, filename, data):
        try:
            file = open(filename,"a+")
            file.write(data)
            file.close()
        except Exception as e:
            log = "Error While writing file"
            self.write_to_file(log_file,str(log))

    def check(self, fileName = None):
        print "checking filename:", fileName
        datafile = file(fileName)
        lines = []
        for line in datafile:
            if re.findall(self.PORT_REGEX, line):
                matched = re.match(self.PORT_REGEX, line)
                if matched:
                    port = matched.group(1)
                    self.PORTS.append(port)
                else:
                    self.write_to_file(log_file,"Regex match failed") 
                lines.append(line)
        return lines
 
    def find_wwn(self):
        dir_list = os.listdir(self.work_dir)
        all_files = []
        for root,dirs,files in os.walk(self.work_dir):
            try:
                if type(files) == list:
                    for temp_file in files:
                        all_files.append(os.path.join(root, temp_file))
            except Exception as e:
                self.write_to_file(log_file,"Error While getting files :  %s" % (str(e)))
        all_items = []
        for item in all_files:
            item_list = self.check(item)
            all_items.extend(item_list)
        uwwn = list(set(self.PORTS))
        return uwwn

