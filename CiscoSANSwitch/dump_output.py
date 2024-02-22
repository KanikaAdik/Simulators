#!/usr/bin/env python
import paramiko, sys, os, getopt, json, subprocess, glob, re
from paramiko.ssh_exception import AuthenticationException, SSHException
from RemoteCommand import *

#SSH Probe, get CONF PERF File 
def usage():
    print ("""\
USAGE:
    %(filename)s -- [OPTIONS]

OPTIONS
    -h, --help
        Display Usage Information
    -c, --ciscoIP
        CSAN Probe ip

    """ % {'filename' : os.path.basename(__file__)}
)
opts, task_list = getopt.getopt(sys.argv[1:],
    "hc:c",
    ["help", "ciscoIP="])

ciscoIP = None

for opt, value in opts:
    if opt in ("-h", "--help"):
        usage()
        sys.exit(0)
    elif opt in ("-c", "--ciscoIP"):
        ciscoIP = value

rc = RemoteCommand(hostIP, username, password)
rc.ssh_connect()
show_commands = "cat *.xml | grep 'show'| sort -u"
commands = []

def write_to_file(dir, command, output):
    command = command.replace(" ", "_")
    command=os.path.join(dir, command)
    with open(command, 'w') as fp:
         fp.write(output)

#get show commands in a text file
rc.execute("cd /usr/local/megha/lib/ciscoSANSwitch && %s"% show_commands)
text = rc.get_std_out()
for each in filter(None,text.split('\n')):
    match = re.match(r'.*?command=\"(.*?show.*?)\".*?$',each)
    commands.append(match.group(1))

#SSH Cisco SAN Switch, trigger command fetch output & dump in a file
#store file in Folder with CSAN Probe type
print ("connecting",  ciscoIP)
cisco_rc = RemoteCommand(ciscoIP, 'cliprobe','Cliprobe@123')

cisco_rc.execute("show hardware")
for each in filter(None,cisco_rc.get_std_out().split('\n')):
    match = re.match(r'.*?cisco(.*?)FC.*?$',each)
    if match :
        match=match.group(1).strip()
        dirname = match.replace(" ","_")
        break
print (dirname)
dir = os.path.join(os.getcwd(),dirname)

if not os.path.exists(dir):
    os.makedirs(dir)
for command in commands:
    cisco_rc.execute(command)
    print ("this is die:", dir)
    write_to_file(dir, command, cisco_rc.get_std_out())
