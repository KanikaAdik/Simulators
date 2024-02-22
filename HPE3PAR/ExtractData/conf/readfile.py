import re, os,sys

thisdir = os.path.join(os.getcwd(), "TXTFILE")
files = os.listdir(thisdir)
files = [afile for afile in files if os.path.isfile(afile)]



for afile in files:
     filename = afile.split(".")[0]
     fl = os.path.join(os.getcwd(),"dumps",filename)
     if not os.path.exists(fl):
         os.mkdir(fl)
     with open(afile) as fr:
         lines = fr.readlines()
     flag =0
     command = ""
     contents =[]
     for each in lines:
          if each == "" :
              continue
          if "3Par7450 cli%" in each:
              flag = 1
              try:
                  each = [wrd.strip('\r\n') for wrd in each.split(" ") if wrd != '']
                  cmd = each[2]
              except:
                  pass
                  continue
              try:
                  command = ('').join(each[3:]).strip('\r\n')
              except:
                  pass
              if command=="":
                  command = cmd 
              else:
                  command = cmd+command.strip(" ")
          elif flag == 0:
              continue
          elif len(re.findall('[/]{6}', each))>0:
              flag =0
              if command == "":
                  continue
              path = os.path.join(fl, command)
              fh=open(path,"w")
              fh.write(('').join(contents))
              fh.close()
              contents =[] 
          elif flag ==1:
              contents.append(each)
              #print command,">>>>>>>>>>>>>>>>>>>>>>",  contents
