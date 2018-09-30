import xmlschema, os
from pprint import pprint
import xml.etree.ElementTree as ET
from xml.etree import ElementTree as et

xmlFile = "CC515A_Intrasoft_Submission_As_String_Case_Edit.xml"

def xml_Read_Validate(xmlFile):
    xsdFile = 'CC515A.xsd'
    #xsdFile = 'test.xsd'; xmlFile = 'test.xml'

    schema_xsd = open(xsdFile).read()
    schema = xmlschema.XMLSchema(schema_xsd)

    """
    print('schema types : ' + 100*'%')
    print(schema.types)
    print('dict: schema elements'+ 100*'%')
    pprint(dict(schema.elements))
    print('schema attributes'+ 100*'%')
    print(schema.attributes)
    print('more'+ 100*'%')
    pprint(sorted(schema.maps.types.keys())[:5])
    pprint(sorted(schema.maps.elements.keys())[:10])
    """

    print(schema.is_valid(xmlFile))
    pprint(schema.to_dict(xmlFile))

def xml_Edit_Info():
    """
    tree = ET.parse(xmlFile)
    a = tree.find('TRAEXPEX1')
    for b in a.findall('NamEX17'):
        if b.text.strip() == 'Gio':
            break
    else:
        ET.SubElement(a, "NamEX17").text = "Gio"
    tree.write(xmlFile)
    """

    tree = et.parse(xmlFile)
    tree.find('.//NamTDE1').text = 'Giovanni'
    tree.find('.//NamEX17').text = 'Rivaldo'
    tree.write('Edited_' + xmlFile)

    xml_Read_Validate('Edited_' + xmlFile)

#xml_Read_Validate(xmlFile)
xml_Edit_Info()