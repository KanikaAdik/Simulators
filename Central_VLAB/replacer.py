import os, sys

class replacer():
    def __init__(self, dirname, prev_wwns, new_wwns):
        self.dirname = dirname
        self.prev_wwns = prev_wwns
        self.new_wwns = new_wwns
 
    def create_new_dir(self):
        path = os.path.join(os.getcwd(),self.dirname)
        fileList = os.listdir(path)
        fileList = ['%s'% path+"/"+fil for fil in fileList]
        path = os.path.join(os.getcwd(),self.dirname+"-new")
        os.mkdir(path)
        for afile in fileList:
            os.system('cp %s %s'%(afile,path))
        return path 

    def replace_wwns(self):
        dirname =  self.create_new_dir()
        for p, n in zip(self.prev_wwns, self.new_wwns):
             cmd = "sed -i 's\%s\%s\g' %s/*" % (p,n, dirname)
             print cmd
             os.system(cmd)
        return True
