from wwn_finder import wwn_finder
from generate_wwn import generate_wwn
from replacer import replacer
import os, sys

print sys.argv
folder_name = sys.argv[1]

wwnfind = wwn_finder(folder_name)
wwnlist = wwnfind.find_wwn()


noofwwn = len(wwnlist)

genwwn = generate_wwn(noofwwn)
newwwn = genwwn.get_wwn()

print noofwwn
print wwnlist
print newwwn

rep = replacer(folder_name, wwnlist, newwwn)
status = rep.replace_wwns()

print status

"""
os.system('python wwn_finder.py -d %s '%s folder_name)
os.system('python generate_wwn.py  replacer.py  serach_replace.log  TEST  test.py  wwn_finder.py ')
os.system('python generate_wwn.py  replacer.py  serach_replace.log  TEST  test.py  wwn_finder.py ')
"""
