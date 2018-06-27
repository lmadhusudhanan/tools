#!/usr/local/bin/python3

import yaml
import pdb
import sys

fp = open("test.yaml", "r")

data = yaml.load(fp)
#pdb.set_trace()


#modifications
data["kubeletArguments"]["pods-per-core"] = int(sys.argv[1])

with open("test.yaml", "w") as fp:
    yaml.dump(data, fp)
