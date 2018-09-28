import xmlschema
from pprint import pprint

my_schema = xmlschema.XMLSchema('CC504A.xsd')

print(my_schema)

"""
print(my_schema.is_valid('CC504A.xml'))

my_schema.is_valid('xmlschema/tests/cases/examples/vehicles/vehicles-1_error.xml')

my_schema.validate('xmlschema/tests/cases/examples/vehicles/vehicles-1_error.xml')

xs = xmlschema.XMLSchema('xmlschema/tests/cases/examples/collection/collection.xsd')
pprint(xs.to_dict('xmlschema/tests/cases/examples/collection/collection.xml'))
"""
