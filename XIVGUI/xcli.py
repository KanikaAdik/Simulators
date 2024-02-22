#!/usr/bin/env python

import os, sys, datetime
from RemoteCommand import RemoteCommand


def check_creds(uname, pwd, ip):
   try:
       rc = RemoteCommand(ip, uname,pwd)
       return True
   except AuthenticationException as err:
       print ("Error: LOGIN_FAILURE_USER_FAILED_TO_LOGIN")
       print ("Error: NO_CONNECTION")      
       return False

class AuthenticationException(Exception):
      pass 


def get_perf_stats(command):
     act_time = command.split(" ")[1].split("=")[1]
     count = int(command.split(" ")[2].split("=")[1])
     interval = command.split(" ")[3].split("=")[1]
     if 'host_fc_port' in command:
          command = "statistics_get_host_fc_port"
     elif 'vol' in command:
          command = "statistics_get_vol"
     elif 'local_fc_port' in command:
          command = "statistics_get_local_fc_port"
     elif 'host' in command:
          command = "statistics_get_host"
     dump_file = os.path.join(os.sep,"opt","XIVGUI","dump",command)
     dump_time = "2017-05-07 00:00:00"
     with open(dump_file) as f:
          str = f.read()
     hr = act_time.split(".")[1].split(":")[0]
     min = int(act_time.split(":")[1])
     sec = act_time.split(":")[2]
     for itr in range(count):
          dump_time="2017-05-07 00:%02d:00" % itr
          t = "%s:%02d:%s" %(hr,(min+itr), sec)
          time = "%s %s" % (act_time.split(".")[0],t)
          str = str.replace(dump_time,time)
     return str

    
ip = input('Machine IP/Hostname:')
tail_ip = "SIM_" + ip.split(".")[3]
uname = input('User name:' )
pwd = input('Password:')
print("connecting...")
command = input("XIV_TAF>>>")
if command == 'exit':
   sys.exit()
#status = check_creds(uname, pwd, ip)
status = 'True'
if status:
   while True:
      command = input("XIV_TAF>>>")
      if command=="":
          continue
      if command == 'exit':
          sys.exit()
      if 'statistics_get' in command:
          output = get_perf_stats(command)
          print (output) 
          continue 
      else :
          dump_file = os.path.join(os.sep,"opt","XIVGUI","dump",command)
      if command:
          if command == 'cod_list':
              with open(dump_file) as f:
                 str = f.read()
              date = datetime.datetime.now().strftime ("%Y-%m-%d")
              str = str.replace('2017-05-03', date )
              str = str.replace('1300785', tail_ip )
              print (str)
              continue
          try:
              with open(dump_file) as f:
                  print (f.read().strip())
              continue
          except:
              pass
      if not os.path.exists(dump_file):
          print ("Error:   UNRECOGNIZED_COMMAND")
          print ("Details: Unrecognized command: '%s'" % command)

