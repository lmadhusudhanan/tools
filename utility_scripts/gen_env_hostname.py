#!/usr/bin/python
dict1={}
dict2={}
list1 = []
list2 = []
password = 'c0ntrail123'
os = "redhat70"

for i in range(1,201):
    #dict1["host{0}".format(i)] = password
    #dict2["host{0}".format(i)] = os
    #list1.append("host{0}: \'{1}\'".format(i,os))
    #list1.append("host{0}: \'{1}\'".format(i,password))
    list1.append("host{0}".format(i))



for element in list1:
    print element+","
#print dict2
