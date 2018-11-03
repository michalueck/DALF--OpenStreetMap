Python 3.7.1 (v3.7.1:260ec2c36a, Oct 20 2018, 00:48:40) 
[GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
Type "help", "copyright", "credits" or "license()" for more information.
>>> #code source Udacity - Example on blueprint
import xml.etree.cElementTree as ET
from collections import defaultdict
import re

osm_file = open("map.osm", "r")

street_type_re = re.compile(r'\S+\.?$', re.IGNORECASE)
street_types = defaultdict(int)
regex = re.compile(r'\b\S+\.?', re.IGNORECASE)

expected = ["Strasse", "Weg", "Allee"]

mapping = { "Str":"Strasse",
            "Straße":"Strasse"}

# Search string for the regex. If it is matched and not in the expected list then add this as a key to the set.
def audit_street(street_types, street_name): 
    m = regex.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def is_street_name(elem): # Check if it is a street name
    return (elem.attrib['k'] == "addr:street")

def audit(osm_file): # return the list that satify the above two functions
    osm_file = open("map.osm", "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street(street_types, tag.attrib['v'])

    return street_types

pprint.pprint(dict(audit(osm_file))) # print the existing names

def string_case(s): # change string into titleCase except for UpperCase
    if s.isupper():
        return s
    else:
        return s.title()

# return the updated names
def update_name(name, mapping):
    name = name.split(' ')
    for i in range(len(name)):
        if name[i] in mapping:
            name[i] = mapping[name[i]]
            name[i] = string_case(name[i])
        else:
            name[i] = string_case(name[i])
    
    name = ' '.join(name)
   

    return name

update_street = audit(osm_file) 

# print the updated names
for street_type, ways in update_street.items():
    for name in ways:
        better_name = update_name(name, mapping)
        print (name, "=>", better_name)

