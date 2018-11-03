def audit_tags(osmfile):
    """Audit the osmfile and return sets of node tag keys, node tag values, way tag keys and way tag values"""
    osm_file = open(osmfile, "r")
    node_tags_keys = set()
    node_tags_values = set()
    way_tags_keys = set()
    way_tags_values = set()

    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node": #only check way and node
            for tag in elem.iter('tag'):
                node_tags_keys.add(tag.attrib['k'])
                node_tags_values.add(tag.attrib['v'])
        if elem.tag == "way": #only check way and node
            for tag in elem.iter('tag'):
                way_tags_keys.add(tag.attrib['k'])
                way_tags_values.add(tag.attrib['v'])
    osm_file.close()
    return node_tags_keys, node_tags_values, way_tags_keys, way_tags_values 

osm_file = "map.osm"  
node_tags_keys, node_tags_values, way_tags_keys, way_tags_values  = audit_tags(osm_file)

lower = re.compile(r'^([a-z]|_)*$', re.IGNORECASE)
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$', re.IGNORECASE)
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]', re.IGNORECASE)
# case insensitive search

def tag_keys(tag_keys_set):
    """Return sets of different types of keys"""
    lower_keys = set()
    lower_colon_keys = set()
    problemchars_keys = set()
    others_keys = set()
    
    for key in tag_keys_set:
        if lower.search(key):
            lower_keys.add(key)
        elif lower_colon.search(key):
            lower_colon_keys.add(key)
        elif problemchars.search(key):
            problemchars_keys.add(key)
        else:
            others_keys.add(key)
            
    return lower_keys,lower_colon_keys,problemchars_keys,others_keys

node_lower_keys,node_lower_colon_keys,node_problemchars_keys,node_others_keys = tag_keys(node_tags_keys)

node_key_types = {"total": len(node_tags_keys),"lower":len(node_lower_keys),"lower colon":len(node_lower_colon_keys),"problemchars":len(node_problemchars_keys),"others":len(node_others_keys)}

print ("The number of keys for each type is: ")
pprint.pprint(node_key_types)

