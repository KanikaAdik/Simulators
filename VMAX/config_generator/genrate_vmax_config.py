import os
import sys
import itertools

SAMPLE = "VMAX_Cumulus_##SYM##.properties"
fh = open(SAMPLE)
sample_text = fh.readlines()
fh.close()

UNISAMPLE = "Unisphere_##SYMIP##.properties"
fh = open(UNISAMPLE)
uni_sample_text = fh.readlines()
fh.close()


config = os.path.join(os.getcwd(), "config")
if not os.path.exists(config):
    os.makedirs(config)

uniconfig = os.path.join(os.getcwd(), "config", "Unisphere")
if not os.path.exists(uniconfig):
    os.makedirs(uniconfig)

def ip_range(input_string):
    octets = input_string.split('.')
    chunks = [map(int, octet.split('-')) for octet in octets]
    ranges = [range(c[0], c[1] + 1) if len(c) == 2 else c for c in chunks]
    #print("ranges", ranges) 

    for address in itertools.product(*ranges):
        #print("address:", address)
        yield '.'.join(map(str, address))


try:
    addresses = ip_range(sys.argv[1])
    print("in try adrr", addresses) 

    for address in  addresses:
        zfilled = address.replace('.','').zfill(12)

        filename = os.path.join(config, SAMPLE.replace("##SYM##", zfilled))
        print filename
        #print sample_text.replace("##SYM##", zfilled).replace("##SYMIP##", address)
        fh = open(filename, 'w')
        for line in sample_text:
            fh.write(line.replace("##SYM##", zfilled).replace("##SYMIP##", address))
        fh.close()

        filename = os.path.join(uniconfig, UNISAMPLE.replace("##SYMIP##", address))
        print filename
        #print sample_text.replace("##SYM##", zfilled).replace("##SYMIP##", address)
        fh = open(filename, 'w')
        for line in uni_sample_text:
            fh.write(line.replace("##SYM##", zfilled).replace("##SYMIP##", address))
        fh.close()
except:
    print "Invalid IP range format, please provide input in below format"
    print "ex. 192.168.33-37.1-255"
    print "ex. 192.168.33.1-255"
    print "ex. 192.168.33.1"
