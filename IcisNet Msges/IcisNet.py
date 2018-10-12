import xmlschema, os, json, datetime
from pprint import pprint
import xml.etree.ElementTree as ET
from xml.etree import ElementTree as et
import xmltodict, pandas as pd

if not os.path.exists(os.path.realpath('Output_Icisnet/') + '/' + 'phonograph' + '/'):
    os.makedirs(os.path.realpath('Output_Icisnet/') + '/' + 'phonograph' + '/')

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

def xml_Edit_Info_CC515A(csvIn):

    """
    all_descendants = list(tree.iter())
    tags = []
    for i in all_descendants:
        tags.append(i.tag)

    tagsDF = pd.DataFrame(tags)
    print(tagsDF)
    """

    'Get Orders'
    dfTemplateOrder = pd.read_csv(csvIn, delimiter=',', encoding="cp1252")

    for index, row in dfTemplateOrder.iterrows():
        print(index + 1, dfTemplateOrder.iloc[:, 0].size)

        taricPicker = Pick_TARIC_Template(row)

        xmlFile = taricPicker[0]

        tree = et.parse(xmlFile); l1 = taricPicker[1]; l2 = taricPicker[2]

        if len(l1) == len(l2):
            for i in range(len(l1)):
                if l1[i] == 'DocTypDC21' and str(row['TARIC']) == '95030035':
                    if l2[i] == 'N380':
                        tree.findall('.//' + 'DocTypDC21')[0].text = l2[i]
                    elif l2[i] == 'N705':
                        tree.findall('.//' + 'DocTypDC21')[1].text = l2[i]
                    elif l2[i] == 'Y903':
                        tree.findall('.//' + 'DocTypDC21')[2].text = l2[i]
                    elif l2[i] == 'Y935':
                        tree.findall('.//' + 'DocTypDC21')[3].text = l2[i]
                    elif l2[i] == '1961':
                        tree.findall('.//' + 'DocTypDC21')[4].text = l2[i]

                elif l1[i] == 'DocTypDC21' and str(row['TARIC']) == '95045000':
                    if l2[i] == 'N380':
                        tree.findall('.//' + 'DocTypDC21')[0].text = l2[i]
                    elif l2[i] == 'N705':
                        tree.findall('.//' + 'DocTypDC21')[1].text = l2[i]
                    elif l2[i] == 'Y903':
                        tree.findall('.//' + 'DocTypDC21')[2].text = l2[i]
                    elif l2[i] == 'Y935':
                        tree.findall('.//' + 'DocTypDC21')[3].text = l2[i]
                    elif l2[i] == '1961':
                        tree.findall('.//' + 'DocTypDC21')[4].text = l2[i]
                    elif l2[i] == 'Y904':
                        tree.findall('.//' + 'DocTypDC21')[5].text = l2[i]

                elif l1[i] == 'DocTypDC21' and (str(row['TARIC']) == '84716060' or str(row['TARIC']) == '85184080'):
                    if l2[i] == 'N380':
                        tree.findall('.//' + 'DocTypDC21')[0].text = l2[i]
                    elif l2[i] == 'N705':
                        tree.findall('.//' + 'DocTypDC21')[1].text = l2[i]
                    elif l2[i] == 'Y901':
                        tree.findall('.//' + 'DocTypDC21')[2].text = l2[i]
                    elif l2[i] == '1961':
                        tree.findall('.//' + 'DocTypDC21')[3].text = l2[i]
                else:
                    tree.find('.//' + l1[i]).text = l2[i]

                tree.write(os.path.realpath('Output_Icisnet/') + '/' + 'phonograph' + '/' + str(row['order-id']) + '_' + xmlFile, encoding="UTF-8", xml_declaration=True)
        else:
            print('Error Algomyth Icisnet Fill : l1 and l2 lists have different sizes! Cannot fill the fields ... check the input csv again! ... ')

    #xml_Read_Validate('Output_Icisnet/Edited_' + xmlFile)

def Pick_TARIC_Template(row):

    recN = str(row['recipient-name'])
    spc = str(row['ship-postal-code'])

    if str(row['TARIC']) == '95030035':

        print(str(row['TARIC']), ' ---> ', '95030035', ' row ')

        l1 = ['SynIdeMES1', 'SynVerNumMES2', 'MesSenMES3', 'MesRecMES6', 'DatOfPreMES9', 'TimOfPreMES10',
              'IntConRefMES11', 'TesIndMES18', 'MesIdeMES19', 'MesTypMES20', 'RefNumHEA4', 'TypOfDecHEA24',
              'CouOfDesCodHEA30', 'AgrLocOfGooCodHEA38', 'AgrLocOfGooHEA39', 'CouOfDisCodHEA55', 'InlTraModHEA75',
              'TraModAtBorHEA76', 'IdeOfMeaOfTraAtDHEA78', 'IdeOfMeaOfTraAtDHEA78LNG',
              'IdeOfMeaOfTraCroHEA85', 'IdeOfMeaOfTraCroHEA85LNG', 'NatOfMeaOfTraCroHEA87', 'ConIndHEA96',
              'DiaLanIndAtDepHEA254', 'ECSAccDocHEA601', 'TotNumOfIteHEA305', 'TotNumOfPacHEA306',
              'DecDatHEA383', 'DecPlaHEA394', 'DecPlaHEA394LNG', 'ComRefNumHEA', 'TypOfDecBx12HEA651', 'TIRFolHEA1025',
              'NamEX17', 'StrAndNumEX122', 'PosCodEX123', 'CitEX124', 'CouEX125', 'NADLNGEX', 'TINEX159',
              'NamCE17', 'StrAndNumCE122', 'PosCodCE123', 'CitCE124', 'CouCE125', 'NADLNGCE', 'RefNumERT1',
              'RefNumEXT1', 'IteNumGDS7', 'GooDesGDS23', 'NetMasGDS48', 'ProReqGDI1', 'PreProGDI1',
              'ComNatProGIM1', 'StaValAmoGDI1', 'CouOfOriGDI1',

              'PreDocTypAR21', 'PreDocRefAR26', 'PreDocCatPREADMREF21',
              'DocTypDC21', 'DocRefDC23', 'DocRefDCLNG',
              'DocTypDC21', 'DocRefDC23', 'DocRefDCLNG',
              'DocTypDC21', 'DocRefDC23', 'DocRefDCLNG',
              'DocTypDC21', 'DocRefDC23', 'DocRefDCLNG',
              'DocTypDC21', 'DocRefDC23', 'DocRefDCLNG',

              'ComNomCMD1', 'TARCodCMD1', 'TARFirAddCodCMD1', 'TARSecAddCodCMD1',
              'NAtAddCodCMD1', 'MarNumOfPacGS21', 'MarNumOfPacGS21LNG', 'KinOfPacGS23', 'NumOfPacGS24', 'SpeMenTDE1022',
              'IncCodTDL1', 'ComInfDELTER387', 'ComInfDELTER387LNG', 'CurTRD1', 'TotAmoInvTRD1',
              'ExcRatTRD1', 'RepStatCodSTATREP386']

        l2 = ['UNOC', '3', 'TRADER.GR', 'NXA.GR', datetime.datetime.now().strftime("%y%m%d"), datetime.datetime.now().strftime("%H%M"),
              '1.50105E+12', '0', '1.50105E+12', 'CC515A', str(row['order-id']), 'EX',
              str(row['ship-country']), '01/0102/24', 'phonograph', 'GR', '3', '4',
              'BCS7837', 'DE', 'BCS7837', 'EN', 'DE', '0', 'EL', 'EL', '1', '1',
              datetime.datetime.now().strftime("%Y%m%d"), 'ΤΕΛΩΝΕΙΟ ΑΘΗΝΩΝ', 'EL',
              str(row['order-id']), 'C', '0', 'PHONOGRAPH ΕΠΕ', 'ΛΕΩΦ. ΠΟΣΕΙΔΩΝΟΣ 93', '16674', 'ΓΛΥΦΑΔΑ', 'GR', 'EL', 'GR997728048',
              recN[0:35], str(row['ship-address-1']), spc[0:5], str(row['ship-city']), str(row['ship-country']),
              'EN', 'GR000102', 'GR000304', '1', str(row['product-name']), str(row['NET']), '10', '00', '000',
              str(row['PRICE']).replace(',','.'), 'GR',

              '380', str(row['order-id']), 'Z',

              'N380', str(row['order-id']), 'EN',
              'N705', str(row['TRACKING']), 'EN',
              'Y903', '-', 'EL',
              'Y935', '-', 'EL',
              '1961', '17GR000001SASP00038', 'EL',

              str(row['TARIC']), '00', '4099', '0000', '0000', str(row['TRACKING']),
              'EN', 'PC', '1', '00400', 'FCA', 'ΑΘΗΝΑ', 'EN', str(row['currency']), str("%.2f" % round(row['item-price'] + row['item-tax'] + row['shipping-price'] + row['shipping-tax'], 2)),
              str(row['eurConversion']), '1']

        xmlFile = "CC515A_Phonograph_Template_Submission_95030035.xml"

    elif  str(row['TARIC']) == '95045000':

        print(str(row['TARIC']), ' ---> ', '95045000', ' row ')

        l1 = ['SynIdeMES1', 'SynVerNumMES2', 'MesSenMES3', 'MesRecMES6', 'DatOfPreMES9', 'TimOfPreMES10',
              'IntConRefMES11', 'TesIndMES18', 'MesIdeMES19', 'MesTypMES20', 'RefNumHEA4', 'TypOfDecHEA24',
              'CouOfDesCodHEA30', 'AgrLocOfGooCodHEA38', 'AgrLocOfGooHEA39', 'CouOfDisCodHEA55', 'InlTraModHEA75',
              'TraModAtBorHEA76', 'IdeOfMeaOfTraAtDHEA78', 'IdeOfMeaOfTraAtDHEA78LNG',
              'IdeOfMeaOfTraCroHEA85', 'IdeOfMeaOfTraCroHEA85LNG', 'NatOfMeaOfTraCroHEA87', 'ConIndHEA96',
              'DiaLanIndAtDepHEA254', 'ECSAccDocHEA601', 'TotNumOfIteHEA305', 'TotNumOfPacHEA306',
              'DecDatHEA383', 'DecPlaHEA394', 'DecPlaHEA394LNG', 'ComRefNumHEA', 'TypOfDecBx12HEA651', 'TIRFolHEA1025',
              'NamEX17', 'StrAndNumEX122', 'PosCodEX123', 'CitEX124', 'CouEX125', 'NADLNGEX', 'TINEX159',
              'NamCE17', 'StrAndNumCE122', 'PosCodCE123', 'CitCE124', 'CouCE125', 'NADLNGCE', 'RefNumERT1',
              'RefNumEXT1', 'IteNumGDS7', 'GooDesGDS23', 'NetMasGDS48', 'ProReqGDI1', 'PreProGDI1',
              'ComNatProGIM1', 'StaValAmoGDI1', 'CouOfOriGDI1',

              'PreDocTypAR21', 'PreDocRefAR26', 'PreDocCatPREADMREF21',

              'DocTypDC21', 'DocRefDC23', 'DocRefDCLNG',
              'DocTypDC21', 'DocRefDC23', 'DocRefDCLNG',
              'DocTypDC21', 'DocRefDC23', 'DocRefDCLNG',
              'DocTypDC21', 'DocRefDC23', 'DocRefDCLNG',
              'DocTypDC21', 'DocRefDC23', 'DocRefDCLNG',
              'DocTypDC21', 'DocRefDC23', 'DocRefDCLNG',

              'ComNomCMD1', 'TARCodCMD1', 'TARFirAddCodCMD1', 'TARSecAddCodCMD1',
              'NAtAddCodCMD1', 'MarNumOfPacGS21', 'MarNumOfPacGS21LNG', 'KinOfPacGS23', 'NumOfPacGS24', 'SpeMenTDE1022',
              'IncCodTDL1', 'ComInfDELTER387', 'ComInfDELTER387LNG', 'CurTRD1', 'TotAmoInvTRD1',
              'ExcRatTRD1', 'RepStatCodSTATREP386']

        l2 = ['UNOC', '3', 'TRADER.GR', 'NXA.GR', datetime.datetime.now().strftime("%y%m%d"),
              datetime.datetime.now().strftime("%H%M"),
              '1.50105E+12', '0', '1.50105E+12', 'CC515A', str(row['order-id']), 'EX',
              str(row['ship-country']), '01/0102/24', 'phonograph', 'GR', '3', '4',
              'BCS7837', 'DE', 'BCS7837', 'EN', 'DE', '0', 'EL', 'EL', '1', '1',
              datetime.datetime.now().strftime("%Y%m%d"), 'ΤΕΛΩΝΕΙΟ ΑΘΗΝΩΝ', 'EL',
              str(row['order-id']), 'C', '0', 'PHONOGRAPH ΕΠΕ', 'ΛΕΩΦ. ΠΟΣΕΙΔΩΝΟΣ 93', '16674', 'ΓΛΥΦΑΔΑ', 'GR', 'EL',
              'GR997728048',
              recN[0:35], str(row['ship-address-1']), spc[0:5], str(row['ship-city']), str(row['ship-country']),
              'EN', 'GR000102', 'GR000304', '1', str(row['product-name']), str(row['NET']), '10',
              '00', '000',
              str(row['PRICE']).replace(',','.'), 'GR',

              '380', str(row['order-id']), 'Z',

              'N380', str(row['order-id']), 'EN',
              'N705', str(row['TRACKING']), 'EN',
              'Y903', '-', 'EL',
              'Y935', '-', 'EL',
              '1961', '17GR000001SASP00038', 'EL',
              'Y904', '-', 'EL',

              str(row['TARIC']), '00', '4099', '0000', '0000', str(row['TRACKING']),
              'EN', 'PC', '1', '00400', 'FCA', 'ΑΘΗΝΑ', 'EN', str(row['currency']),
              str("%.2f" % round(row['item-price'] + row['item-tax'] + row['shipping-price'] + row['shipping-tax'], 2)),
              str(row['eurConversion']), '1']

        xmlFile = "CC515A_Phonograph_Template_Submission_95045000.xml"

    elif str(row['TARIC']) == '84716060' or str(row['TARIC']) == '85184080':

        print(str(row['TARIC']), ' ---> ', '84716060 OR 85184080', ' row ')

        l1 = ['SynIdeMES1', 'SynVerNumMES2', 'MesSenMES3', 'MesRecMES6', 'DatOfPreMES9', 'TimOfPreMES10',
              'IntConRefMES11', 'TesIndMES18', 'MesIdeMES19', 'MesTypMES20', 'RefNumHEA4', 'TypOfDecHEA24',
              'CouOfDesCodHEA30', 'AgrLocOfGooCodHEA38', 'AgrLocOfGooHEA39', 'CouOfDisCodHEA55', 'InlTraModHEA75',
              'TraModAtBorHEA76', 'IdeOfMeaOfTraAtDHEA78', 'IdeOfMeaOfTraAtDHEA78LNG',
              'IdeOfMeaOfTraCroHEA85', 'IdeOfMeaOfTraCroHEA85LNG', 'NatOfMeaOfTraCroHEA87', 'ConIndHEA96',
              'DiaLanIndAtDepHEA254', 'ECSAccDocHEA601', 'TotNumOfIteHEA305', 'TotNumOfPacHEA306',
              'DecDatHEA383', 'DecPlaHEA394', 'DecPlaHEA394LNG', 'ComRefNumHEA', 'TypOfDecBx12HEA651', 'TIRFolHEA1025',
              'NamEX17', 'StrAndNumEX122', 'PosCodEX123', 'CitEX124', 'CouEX125', 'NADLNGEX', 'TINEX159',
              'NamCE17', 'StrAndNumCE122', 'PosCodCE123', 'CitCE124', 'CouCE125', 'NADLNGCE', 'RefNumERT1',
              'RefNumEXT1', 'IteNumGDS7', 'GooDesGDS23', 'NetMasGDS48', 'ProReqGDI1', 'PreProGDI1',
              'ComNatProGIM1', 'StaValAmoGDI1', 'CouOfOriGDI1', 'SupUniGDI1',

              'PreDocTypAR21', 'PreDocRefAR26', 'PreDocCatPREADMREF21',

              'DocTypDC21', 'DocRefDC23', 'DocRefDCLNG',
              'DocTypDC21', 'DocRefDC23', 'DocRefDCLNG',
              'DocTypDC21', 'DocRefDC23', 'DocRefDCLNG',
              'DocTypDC21', 'DocRefDC23', 'DocRefDCLNG',

              'ComNomCMD1', 'TARCodCMD1', 'TARFirAddCodCMD1', 'TARSecAddCodCMD1',
              'NAtAddCodCMD1', 'MarNumOfPacGS21', 'MarNumOfPacGS21LNG', 'KinOfPacGS23', 'NumOfPacGS24', 'SpeMenTDE1022',
              'IncCodTDL1', 'ComInfDELTER387', 'ComInfDELTER387LNG', 'CurTRD1', 'TotAmoInvTRD1',
              'ExcRatTRD1', 'RepStatCodSTATREP386']

        l2 = ['UNOC', '3', 'TRADER.GR', 'NXA.GR', datetime.datetime.now().strftime("%y%m%d"),
              datetime.datetime.now().strftime("%H%M"),
              '1.50105E+12', '0', '1.50105E+12', 'CC515A', str(row['order-id']), 'EX',
              str(row['ship-country']), '01/0102/24', 'phonograph', 'GR', '3', '4',
              'BCS7837', 'DE', 'BCS7837', 'EN', 'DE', '0', 'EL', 'EL', '1', '1',
              datetime.datetime.now().strftime("%Y%m%d"), 'ΤΕΛΩΝΕΙΟ ΑΘΗΝΩΝ', 'EL',
              str(row['order-id']), 'C', '0', 'PHONOGRAPH ΕΠΕ', 'ΛΕΩΦ. ΠΟΣΕΙΔΩΝΟΣ 93', '16674', 'ΓΛΥΦΑΔΑ', 'GR', 'EL',
              'GR997728048',
              recN[0:35], str(row['ship-address-1']), spc[0:5], str(row['ship-city']), str(row['ship-country']),
              'EN', 'GR000102', 'GR000304', '1', str(row['product-name']), str(row['NET']), '10',
              '00', '000',
              str(row['PRICE']).replace(',','.'), 'GR', '1',

              '380', str(row['order-id']), 'Z',

              'N380', str(row['order-id']), 'EN',
              'N705', str(row['TRACKING']), 'EN',
              'Y901', '-', 'EL',
              '1961', '17GR000001SASP00038', 'EL',

              str(row['TARIC']), '00', '0000', '0000', '0000', str(row['TRACKING']),
              'EN', 'PC', '1', '00400', 'FCA', 'ΑΘΗΝΑ', 'EN', str(row['currency']),
              str("%.2f" % round(row['item-price'] + row['item-tax'] + row['shipping-price'] + row['shipping-tax'], 2)),
              str(row['eurConversion']), '1']

        xmlFile = "CC515A_Phonograph_Template_Submission_84716060-85184080.xml"

    return [xmlFile, l1, l2]


def clearFolderData(mypath):
    for root, dirs, files in os.walk(mypath):
        for file in files:
            os.remove(os.path.join(root, file))

def Run_C_Icisnet():
    IcisNetPath = os.path.realpath('Output_Icisnet/')
    clearFolderData(IcisNetPath)

    xsdFileIn = 'CC515A.xsd'
    xml_Edit_Info_CC515A('OrdersIn/'+'ManageOrders121018a.csv')

    #xml_Read_Validate(os.path.realpath('Output_Icisnet/') + '/' + '111-0097454-1677011_CC515A_Phonograph_Template_Submission.xml', xsdFileIn)

def Run_Y_IcisNet():
    dfTemplateOrder = pd.read_csv('templateOrders.csv', delimiter=',', encoding="cp1252")
    dfOrderMRN = pd.read_csv('ORDERMRN.csv', delimiter=',')

    'Group orders by ship-country and currency'
    for index, row in dfOrderMRN.iterrows():
        print(row['order-id'])
        print(row['mrn'])
        break

    """
    'Group orders by ship-country and currency'
    for index, row in dfTemplateOrder.iterrows():
        print(index + 1, dfTemplateOrder.iloc[:, 0].size)

        print(str(row['ship-country'])+'-'+str(row['currency']))
    """

Run_C_Icisnet()
#Run_Y_IcisNet()

"""
#Sample l2
l2 = ['UNOC', '3', 'TRADER.GR', 'NXA.GR', '170726', '955', '1.50105E+12', '0', '1.50105E+12', 'CC515A',
      '1.53856E+12', 'EX', 'CA', '01/0102/24', 'phonograph', 'GR', '3', '4', 'BCS7837', 'DE', 'BCS7837', 'EN',
      'DE', '0', 'EL', 'EL', '1', '1', '1', '20181003', 'ΤΕΛΩΝΕΙΟ ΑΘΗΝΩΝ', 'EL', '701-9454426-6350649', 'C', '0',
      'PHONOGRAPH ΕΠΕ', 'ΛΕΩΦ. ΠΟΣΕΙΔΩΝΟΣ 93', '16674', 'ΓΛΥΦΑΔΑ', 'GR', 'EL', 'GR997728048', 'Philip Santos',
      '510 Goodale Drive.', 'R1N 3M3', 'Portage la Prairie, Manitoba', 'CA', 'EN', 'GR000102', 'GR000304', '1',
      'ΠΑΙΧΝΙΔΙΑ Ubisoft Maria Ubisoft Aguilar', '1', '0.7', '10', '0', '0', '73.65', 'GR', '380',
      '701-9454426-6350649', 'Z', 'N380', '701-9454426-6350649', 'EN''N705', '2647541433', 'EN', 'Y903', '-', 'EL',
      'Y935', '-', 'EL',
      '1961', '17GR000001SASP00038', 'EL', '95030035', '0', '4099', '0', '0', '2647541433', 'EN', 'PC', '1', '400',
      'FCA', 'ΑΘΗΝΑ', 'EN', 'CAD', '111.4', '1.5126', '1']
#More Notes
'Concat the two lists in a pandas DataFrame'
df1 = pd.concat([pd.DataFrame(l1), pd.DataFrame(l2)], axis=1)

"""