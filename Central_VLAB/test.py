import re

regex   = ".*?gTokenId = \"(.*?)\";.*?$"

line = "interface fc1/4 swwn 20:00:00:2a:6a:3b:95:80"
#PORT_REGEX = ".*?(([0-9a-f]{2}[:-]){7}([0-9a-f]{2}))\w+.*?"

#PORT_REGEX = ".*?(([0-9a-f]{2}[:-]){7})\w+.*?"

#PORT_REGEX = '.*?(([0-9A-Fa-f]{2}[:-]{7})[0-9A-Fa-f]{2}).*?'
PORT_REGEX = '.*?(([0-9A-Fa-f]{2}[:-]){7}[0-9A-Fa-f]{2}).*?'

matched = re.match(PORT_REGEX, line)
print matched
if matched:
    print "MATCH"
    #print dir(matched)
    #print dir(matched.group)
    print matched.group(1)
else:
    print "No Match"
