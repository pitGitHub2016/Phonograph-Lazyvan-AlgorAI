from lxml import etree, objectify
from lxml.etree import XMLSyntaxError

def xml_validator(some_xml_string, xsd_file='/path/to/my_schema_file.xsd'):
    try:
        schema = etree.XMLSchema(file=xsd_file)
        parser = objectify.makeparser(schema=schema)
        objectify.fromstring(some_xml_string, parser)
        print "YEAH!, my xml file has validated"
    except XMLSyntaxError:
        #handle exception here
        print "Oh NO!, my xml file does not validate"
        pass

xml_file = open('my_xml_file.xml', 'r')
xml_string = xml_file.read()
xml_file.close()

xml_validator(xml_string, '/path/to/my_schema_file.xsd')

"""
import xmlschema, os
from pprint import pprint

schema_xsd = open('CC504A.xsd').read()
schema = xmlschema.XMLSchema(schema_xsd)

print(schema.types)
pprint(dict(schema.elements))
print(schema.attributes)
pprint(sorted(schema.maps.types.keys())[:5])
pprint(sorted(schema.maps.elements.keys())[:10])

#///////////////////////////////////////////
my_schema.is_valid('xmlschema/tests/cases/examples/vehicles/vehicles-1_error.xml')

my_schema.validate('xmlschema/tests/cases/examples/vehicles/vehicles-1_error.xml')

xs = xmlschema.XMLSchema('xmlschema/tests/cases/examples/collection/collection.xsd')
pprint(xs.to_dict('xmlschema/tests/cases/examples/collection/collection.xml'))
"""
