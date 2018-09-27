from PyPDF2 import PdfFileWriter, PdfFileReader
import io, requests
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
import urllib, pandas as pd

def fetchWixDB_UserDocsUploads():
    r = requests.get('https://gekko1990.wixsite.com/cn23/_functions/UserDocsUploads_algomyth_GAK2018')
    resp = r.json()
    for i in resp['items']:
        #print(i)
        try:
            d0 = i['userId']
            dm1 = i['field'].split('/')
            fileName = dm1[-1]
            fileWixID = dm1[-2]

            urlWix = 'https://static.wixstatic.com/ugd/'+fileWixID
            urllib.request.urlretrieve(urlWix, fileWixID.split('.')[0]+'-'+fileName)
        except:
            pass

def testWixExcelDataRead():
    df = pd.read_excel('Users_OrdersUploads/'+'d2c771_2b911bcd1cd44994921d1a62c8468391-wixCN23_Test_amazon.xlsx')
    #print(df.columns)

    userId = '123456789'
    dataSender = {'Name': 'Alexander Belles', 'VAT': 'GR997728048', 'Business': 'Phonograph', 'Street': 'Poseidwnos',
                  'TelNo': '2109090900', 'PostCode': '18479', 'City': 'Athens', 'Country': 'Greece'}

    for index, row in df.iterrows():
        print(index+1, df['buyer-name'].size)

        dataReceiver = {'Name': str(row['buyer-name']), 'Business': str(row['buyer-name']), 'Street': str(row['ship-address-1']),
                    'TelNo': str(row['buyer-phone-number']), 'PostCode': str(row['ship-postal-code']), 'City': str(row['ship-city']), 'Country': str(row['ship-country'])}
        dataProductsInfo = {'prodDescription': str(row['product-name']), 'prodQuantity': str(row['quantity-purchased']), 'prodWeight': 'None' + ' ' + 'kg',
                        'prodValue': str(row['currency']) + ' ' + str(row['item-price']), 'prodHSTarif': '', 'prodCountryOfOrigin': str(row['ship-country'])}
        dataProductCategory = 'x'
        dataComments = '-'
        dataLicense = '-'
        dataCertificate = '-'
        dataInvoice = {'tick': 'x', 'val': 'INV000'+str(index+1)}

        cn23_dataIn = [dataSender, dataReceiver, dataProductsInfo, dataProductCategory, dataComments, dataLicense, dataCertificate, dataInvoice]

        CN23_PDF(userId, str(index), cn23_dataIn)
        break

def CN23_PDF(userId, cn23_idx, dataIn):

    dataSender = dataIn[0]; dataReceiver = dataIn[1]
    dataProductsInfo = dataIn[2]; dataProductCategory = dataIn[3]
    dataComments = dataIn[4]; dataLicense = dataIn[5]; dataCertificate = dataIn[6]
    dataInvoice = dataIn[7]

    # Registered font family
    pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
    pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
    pdfmetrics.registerFont(TTFont('VeraIt', 'VeraIt.ttf'))
    pdfmetrics.registerFont(TTFont('VeraBI', 'VeraBI.ttf'))
    # Registered fontfamily
    registerFontFamily('Vera',normal='Vera',bold='VeraBd',italic='VeraIt',boldItalic='VeraBI')

    packet = io.BytesIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=letter)

    fontSettings = [10, 8, 6, 4, 2]
    can.setFont('Vera', fontSettings[0])

    'Sender Info'
    can.drawString(86, 788, dataSender['Name'])
    can.drawString(84, 773, dataSender['Business'])

    can.setFont('Vera', fontSettings[1])
    can.drawString(254, 773, dataSender['VAT'])

    can.setFont('Vera', fontSettings[0])
    can.drawString(84, 758, dataSender['Street'])
    can.drawString(230, 758, dataSender['TelNo'])
    can.drawString(120, 744, dataSender['PostCode'])
    can.drawString(200, 744, dataSender['City'])
    can.drawString(84, 729, dataSender['Country'])
    'Receiver Info'
    can.drawString(84, 714, dataReceiver['Name'])
    can.drawString(84, 700, dataReceiver['Business'])
    can.drawString(80, 685, dataReceiver['Street'])
    can.drawString(225, 685, dataReceiver['TelNo'])
    can.drawString(120, 670, dataReceiver['PostCode'])
    can.drawString(200, 670, dataReceiver['City'])
    can.drawString(84, 655, dataReceiver['Country'])
    '1st Product info'

    print(len(dataProductsInfo['prodDescription']))
    if len(dataProductsInfo['prodDescription']) > 25 and len(dataProductsInfo['prodDescription']) < 30:
        can.setFont('Vera', fontSettings[1])
    elif len(dataProductsInfo['prodDescription']) > 30 and len(dataProductsInfo['prodDescription']) < 40:
        can.setFont('Vera', fontSettings[2])
    elif len(dataProductsInfo['prodDescription']) > 40 and len(dataProductsInfo['prodDescription']) < 80:
        can.setFont('Vera', fontSettings[3])
    can.drawString(54, 618, dataProductsInfo['prodDescription'])

    can.setFont('Vera', fontSettings[0])
    can.drawString(204, 618, dataProductsInfo['prodQuantity'])
    can.drawString(250, 618, dataProductsInfo['prodWeight'])
    can.drawString(310, 618, dataProductsInfo['prodValue'])
    can.drawString(370, 618, dataProductsInfo['prodHSTarif'])
    can.drawString(470, 618, dataProductsInfo['prodCountryOfOrigin'])
    """
    '2nd Product info'
    can.drawString(54, 618, dataProductsInfo['prodDescription'])
    can.drawString(204, 618, dataProductsInfo['prodQuantity'])
    can.drawString(250, 618, dataProductsInfo['prodWeight'])
    can.drawString(320, 618, dataProductsInfo['prodValue'])
    can.drawString(370, 618, dataProductsInfo['prodHSTarif'])
    can.drawString(470, 618, dataProductsInfo['prodCountryOfOrigin'])
    '3rd Product info'
    can.drawString(54, 618, dataProductsInfo['prodDescription'])
    can.drawString(204, 618, dataProductsInfo['prodQuantity'])
    can.drawString(250, 618, dataProductsInfo['prodWeight'])
    can.drawString(320, 618, dataProductsInfo['prodValue'])
    can.drawString(370, 618, dataProductsInfo['prodHSTarif'])
    can.drawString(470, 618, dataProductsInfo['prodCountryOfOrigin'])
    '4th Product info'
    can.drawString(54, 618, dataProductsInfo['prodDescription'])
    can.drawString(204, 618, dataProductsInfo['prodQuantity'])
    can.drawString(250, 618, dataProductsInfo['prodWeight'])
    can.drawString(320, 618, dataProductsInfo['prodValue'])
    can.drawString(370, 618, dataProductsInfo['prodHSTarif'])
    can.drawString(470, 618, dataProductsInfo['prodCountryOfOrigin'])
    """
    'Product Comments'
    can.drawString(54, 502, dataComments)
    'Product Category'
    can.drawString(115, 525, dataProductCategory)
    'Product Invoice'
    can.drawString(249, 463, dataInvoice['tick'])
    can.drawString(250, 448, dataInvoice['val'])

    can.save()

    #move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(open("CN23_template.pdf", "rb"))
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    # finally, write "output" to a real file
    outputStream = open("CN23_Out/"+userId+"-"+cn23_idx+"-CN23.pdf", "wb")
    output.write(outputStream)
    outputStream.close()

#fetchWixDB()
testWixExcelDataRead()