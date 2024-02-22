import re, json, os, sys, subprocess

class nas_run():
    def __init__(self,args=[],out_dir=None):
        self.args = args
        self._out_dir = out_dir
        self.log_file = os.path.join(os.sep,"nas","bin","probe.log")

    def write_to_file(self,filename, data):
        file = open(filename,"a+")
        file.write(data)
        file.close()

    def _run(self):
        if not (len(sys.argv) > 1):
            sys.exit(0)

        file = None

        for item in sys.argv[1:]:
            if not file:
                file = item.strip("-")
            else:
                file = "%s_%s" % (file,item.strip("-"))

            dump_file = os.path.join(os.sep,"nas","bin","vnxFile",self._out_dir,file)

        #print dump_file
        self._print_contents(dump_file)
       
    def _get_details(self,type="serial"):
        ip = None
        proc = subprocess.Popen(["echo $SSH_CONNECTION"], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        if err:
            self.write_to_file(self.log_file, "Error While giving serial number\n")
        else:
            try:
                out_list = out.split(" ")
                serial_ip = out_list[2]
                ip_adress = "".join(serial_ip.split("."))
                serial_num = "APM00%s" % (ip_adress)
            except Exception as e:
                self.write_to_file(self.log_file, "Error While giving serial number : %s\n" % str(e))

        if type == "serial_num":
            return serial_num
        else:
            return ip_adress

    def _print_contents(self,dump_file): 
        if os.path.exists(dump_file):
             #print "Dump FIle COntents"
             self.write_to_file(self.log_file, "File Dumping : %s\n" % dump_file)
             serial_no = self._get_details(type="serial")
             ip_adress = self._get_details(type="ip")
             with open(dump_file) as f:
                 contents = f.read() 
                 dump_contents = contents.replace("$$$$",serial_no)
                 final_contents = dump_contents.replace("####", ip_adress)
                 print final_contents
                 
        else:
            self.write_to_file(self.log_file, "File Does Not Exists : %s\n" % dump_file)
         
    def getItem(self,item=None):
        newItem = None
        for each in item.split(","):
            if newItem:
                newItem = "%s_%s" % (newItem, each)
            else:
                newItem = each

        return newItem
   
    def _server_stats_run(self):
         if not (len(sys.argv) > 1):
             sys.exit(0)

         file = None

         for item in sys.argv[1:]:
             if not file:
                 item = self.getItem(item)
                 file = item.strip("-")
             else:
                 item = self.getItem(item)
                 file = "%s_%s" % (file,item.strip("-"))

         dump_file = os.path.join(os.sep,"nas","bin","vnxFile",self._out_dir,file)

         self._print_contents(dump_file)
 
    
