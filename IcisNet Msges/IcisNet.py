import xmlschema, os, json
from pprint import pprint
import xml.etree.ElementTree as ET
from xml.etree import ElementTree as et
import xmltodict, pandas as pd

def xml_Read_Validate(xsdFile, xmlFile):

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

def xml_Edit_Info_CC515A(xmlFile):

    tree = et.parse(xmlFile)

    """
    all_descendants = list(tree.iter())
    tags = []
    for i in all_descendants:
        tags.append(i.tag)

    tagsDF = pd.DataFrame(tags)
    print(tagsDF)
    """

    l1 = ['SynIdeMES1', 'SynVerNumMES2', 'MesSenMES3', 'MesRecMES6', 'DatOfPreMES9', 'TimOfPreMES10', 'IntConRefMES11',
          'TesIndMES18', 'MesIdeMES19', 'MesTypMES20', 'RefNumHEA4', 'TypOfDecHEA24',
          'CouOfDesCodHEA30', 'AgrLocOfGooCodHEA38', 'AgrLocOfGooHEA39', 'CouOfDisCodHEA55', 'InlTraModHEA75',
          'TraModAtBorHEA76', 'IdeOfMeaOfTraAtDHEA78', 'IdeOfMeaOfTraAtDHEA78LNG',
          'IdeOfMeaOfTraCroHEA85', 'IdeOfMeaOfTraCroHEA85LNG', 'NatOfMeaOfTraCroHEA87', 'ConIndHEA96',
          'DiaLanIndAtDepHEA254', 'ECSAccDocHEA601', 'TotNumOfIteHEA305', 'TotNumOfPacHEA306', 'TotGroMasHEA307',
          'DecDatHEA383', 'DecPlaHEA394', 'DecPlaHEA394LNG', 'ComRefNumHEA', 'TypOfDecBx12HEA651', 'TIRFolHEA1025',
          'NamEX17', 'StrAndNumEX122', 'PosCodEX123', 'CitEX124', 'CouEX125', 'NADLNGEX', 'TINEX159',
          'NamCE17', 'StrAndNumCE122', 'PosCodCE123', 'CitCE124', 'CouCE125', 'NADLNGCE', 'RefNumERT1', 'RefNumEXT1',
          'IteNumGDS7', 'GooDesGDS23', 'GroMasGDS46', 'NetMasGDS48', 'ProReqGDI1', 'PreProGDI1',
          'ComNatProGIM1', 'StaValAmoGDI1', 'CouOfOriGDI1', 'PreDocTypAR21', 'PreDocRefAR26', 'PreDocCatPREADMREF21',
          'DocTypDC21', 'DocRefDC23', 'DocRefDCLNG', 'DocTypDC21', 'DocRefDC23', 'DocRefDCLNG',
          'DocTypDC21', 'DocRefDC23', 'DocRefDCLNG', 'DocTypDC21', 'DocRefDC23', 'DocRefDCLNG', 'DocTypDC21',
          'DocRefDC23', 'DocRefDCLNG', 'ComNomCMD1', 'TARCodCMD1', 'TARFirAddCodCMD1', 'TARSecAddCodCMD1',
          'NAtAddCodCMD1', 'MarNumOfPacGS21', 'MarNumOfPacGS21LNG', 'KinOfPacGS23', 'NumOfPacGS24', 'SpeMenTDE1022',
          'IncCodTDL1', 'ComInfDELTER387', 'ComInfDELTER387LNG', 'CurTRD1', 'TotAmoInvTRD1',
          'ExcRatTRD1', 'RepStatCodSTATREP386']

    l2 = ['UNOC', '3', 'TRADER.GR', 'NXA.GR', '170726', '955', '1.50105E+12', '0', '1.50105E+12', 'CC515A',
          '1.53856E+12', 'EX', 'CA', '01/0102/24', 'phonograph', 'GR', '3', '4', 'BCS7837', 'DE', 'BCS7837', 'EN',
          'DE', '0', 'EL', 'EL', '1', '1', '1', '20181003', 'ΤΕΛΩΝΕΙΟ ΑΘΗΝΩΝ', 'EL', '701-9454426-6350649', 'C', '0',
          'PHONOGRAPH ΕΠΕ', 'ΛΕΩΦ. ΠΟΣΕΙΔΩΝΟΣ 93', '16674', 'ΓΛΥΦΑΔΑ', 'GR', 'EL', 'GR997728048', 'Philip Santos',
          '510 Goodale Drive.', 'R1N 3M3', 'Portage la Prairie, Manitoba', 'CA', 'EN', 'GR000102', 'GR000304', '1',
          'ΠΑΙΧΝΙΔΙΑ Ubisoft Maria Ubisoft Aguilar', '1', '0.7', '10', '0', '0', '73.65', 'GR', '380',
          '701-9454426-6350649', 'Z', 'N380', '701-9454426-6350649', 'EN''N705', '2647541433', 'EN', 'Y903', '-', 'EL', 'Y935', '-', 'EL',
          '1961', '17GR000001SASP00038', 'EL', '95030035', '0', '4099', '0', '0', '2647541433', 'EN', 'PC', '1', '400',
          'FCA', 'ΑΘΗΝΑ', 'EN', 'CAD', '111.4', '1.5126', '1']

    df1 = pd.concat([pd.DataFrame(l1), pd.DataFrame(l2)], axis=1)
    print(df1)

    #tree.find('.//SynIdeMES1').text = 'Giovanni'

    #tree.write('Edited_' + xmlFile)

    #xml_Read_Validate('Output_Icisnet/Edited_' + xmlFile)

xsdFileIn = 'CC515A.xsd'
xmlFileIn = "CC515A_Phonograph_Template_Submission.xml"

'Get Orders'
df0 = pd.read_csv('templateOrders.csv',  delimiter=',', encoding = "cp1252")
print(df0.columns)
#xml_Edit_Info_CC515A(xmlFileIn)

l2 = ['UNOC', '3', 'TRADER.GR', 'NXA.GR', '170726', '955', '1.50105E+12', '0', '1.50105E+12', 'CC515A',
          '1.53856E+12', 'EX', 'CA', '01/0102/24', 'phonograph', 'GR', '3', '4', 'BCS7837', 'DE', 'BCS7837', 'EN',
          'DE', '0', 'EL', 'EL', '1', '1', '1', '20181003', 'ΤΕΛΩΝΕΙΟ ΑΘΗΝΩΝ', 'EL', '701-9454426-6350649', 'C', '0',
          'PHONOGRAPH ΕΠΕ', 'ΛΕΩΦ. ΠΟΣΕΙΔΩΝΟΣ 93', '16674', 'ΓΛΥΦΑΔΑ', 'GR', 'EL', 'GR997728048', 'Philip Santos',
          '510 Goodale Drive.', 'R1N 3M3', 'Portage la Prairie, Manitoba', 'CA', 'EN', 'GR000102', 'GR000304', '1',
          'ΠΑΙΧΝΙΔΙΑ Ubisoft Maria Ubisoft Aguilar', '1', '0.7', '10', '0', '0', '73.65', 'GR', '380',
          '701-9454426-6350649', 'Z', 'N380', '701-9454426-6350649', 'EN''N705', '2647541433', 'EN', 'Y903', '-', 'EL', 'Y935', '-', 'EL',
          '1961', '17GR000001SASP00038', 'EL', '95030035', '0', '4099', '0', '0', '2647541433', 'EN', 'PC', '1', '400',
          'FCA', 'ΑΘΗΝΑ', 'EN', 'CAD', '111.4', '1.5126', '1']
