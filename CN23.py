#!flask/bin/python
from flask import Flask, render_template, jsonify, json
from PyPDF2 import PdfFileWriter, PdfFileReader
import io, requests
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
import urllib, pandas as pd, sendgrid
import os, re, os.path

#sys.path.insert(0, '/opt/torus-engine/torus/')
ParentPath = os.path.realpath('Users_OrdersUploads/')
CN23_OutPath = os.path.realpath('CN23_Out/')

#app = Flask(__name__)

#@app.route('/')
#def homepage():
#    return render_template('no data')

#@app.route('/PyCn23/<userId>/', methods=['GET'])
def fetchWixData(userId):
    r = requests.get('https://gekko1990.wixsite.com/cn23/_functions/UserDocsUploads_algomyth_GAK2018/'+userId)
    resp = r.json()
    for i in resp['items']:
        #try:
            wixUserEmail = i['userEmail']

            if not os.path.exists(ParentPath + '/' + wixUserEmail + '/'):
                os.makedirs(ParentPath + '/' + wixUserEmail + '/')

            if not os.path.exists(CN23_OutPath + '/' + wixUserEmail + '/'):
                os.makedirs(CN23_OutPath + '/' + wixUserEmail + '/')

            wixQuery = i['userInfoQuery']
            querySplit = wixQuery.split('~')
            wixDataSender = {'Name': querySplit[0], 'VAT': querySplit[2], 'Business': querySplit[1], 'Street': querySplit[3],
                          'TelNo': querySplit[4], 'PostCode': querySplit[5], 'City': querySplit[6], 'Country': querySplit[7]}

            wixField = i['field'].split('/')
            urllib.request.urlretrieve('https://static.wixstatic.com/ugd/' + wixField[-2], ParentPath + '/' + wixUserEmail + '/' + wixField[-2].split('.')[0] + '-' + wixField[-1])
        #except:
        #    pass

    print('Done with Data Requesting / Storing and Formatting from Wix DB')
    parseOrders(wixDataSender, wixUserEmail)

    #jsonfiles = json.loads(df0.to_json(orient='records'))
    #return jsonify({'jsonfiles': jsonfiles})

def parseOrders(dataSender, wixUserEmail):

    for folder in os.walk(ParentPath + '/' + wixUserEmail):
        files = folder[-1]
        for f in files:
            print(ParentPath + '/' + wixUserEmail + '/' + f)
            df = pd.read_excel(ParentPath + '/' + wixUserEmail + '/' + f)

            for index, row in df.iterrows():
                print(index+1, df.iloc[:, 0].size)

                #amazon
                if df.columns[0] == 'order-id':
                    dataReceiver = {'Name': str(row['recipient-name']), 'Business': '', 'Street': str(row['ship-address-1']),
                                'TelNo': str(row['buyer-phone-number']), 'PostCode': str(row['ship-postal-code']), 'City': str(row['ship-city']), 'Country': str(row['ship-country'])}
                    redProdDescr = row['product-name']
                    prodPriceIn = "%.2f" % round(row['Price'],2)
                    dataProductsInfo = {'prodDescription': str(redProdDescr[0:52]), 'prodQuantity': str(row['quantity-purchased']), 'prodWeight': str(row['Product Weight']).replace(',', '.') + ' ' + 'kg',
                                    'prodValue': '€' + ' ' + str(prodPriceIn), 'prodHSTarif': str(row['HS']), 'prodCountryOfOrigin': 'Greece'}
                    marketplace = 'amazon'
                #ebay
                elif df.columns[0] == 'Sales record number':
                    dataReceiver = {'Name': str(row['Buyer full name']), 'Business': '', 'Street': str(row['Delivery address 1']),
                                    'TelNo': str(row['Phone']), 'PostCode': str(row['Delivery postcode']), 'City': str(row['Delivery city']), 'Country': str(row['Delivery country'])}
                    redProdDescr = row['Item title']
                    prodPriceIn = "%.2f" % round(row['Total price'],2)
                    dataProductsInfo = {'prodDescription': str(redProdDescr[0:52]), 'prodQuantity': str(row['Quantity']),
                                        'prodWeight': str(row['Product Weight']).replace(',', '.'), 'prodValue': str(prodPriceIn), 'prodHSTarif': str(row['HS']),
                                        'prodCountryOfOrigin': 'Greece'}
                    marketplace = 'ebay'

                dataProductCategory = 'x'
                dataComments = '-'
                dataLicense = '-'
                dataCertificate = '-'
                dataInvoice = {'tick': 'x', 'val': str(row['User Invoice Number'])}

                cn23_dataIn = [dataSender, dataReceiver, dataProductsInfo, dataProductCategory, dataComments, dataLicense, dataCertificate, dataInvoice]
                CN23_PDF(wixUserEmail, marketplace, str(index), cn23_dataIn)

                #break

def CN23_PDF(userEmail, MarketPlaceId, cn23_idx, dataIn):

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

    fontSettings = [8, 5]
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

    if len(dataReceiver['Street']) >= 28:
        can.setFont('Vera', fontSettings[1])
    can.drawString(80, 685, dataReceiver['Street'])

    can.drawString(225, 685, dataReceiver['TelNo'])
    can.drawString(120, 670, dataReceiver['PostCode'])
    can.drawString(200, 670, dataReceiver['City'])
    can.drawString(84, 655, dataReceiver['Country'])
    '1st Product info'

    if len(dataProductsInfo['prodDescription']) >= 20:
        can.setFont('Vera', fontSettings[1])
    can.drawString(54, 618, dataProductsInfo['prodDescription'])

    can.setFont('Vera', fontSettings[0])
    can.drawString(204, 618, dataProductsInfo['prodQuantity'])
    can.drawString(250, 618, dataProductsInfo['prodWeight'])
    can.drawString(310, 618, dataProductsInfo['prodValue'])
    can.drawString(370, 618, dataProductsInfo['prodHSTarif'])
    can.drawString(470, 618, dataProductsInfo['prodCountryOfOrigin'])
    
    '2nd Product info'
    #can.drawString(54, 618, dataProductsInfo['prodDescription'])
    #can.drawString(204, 618, dataProductsInfo['prodQuantity'])
    #can.drawString(250, 618, dataProductsInfo['prodWeight'])
    #can.drawString(320, 618, dataProductsInfo['prodValue'])
    #can.drawString(370, 618, dataProductsInfo['prodHSTarif'])
    #can.drawString(470, 618, dataProductsInfo['prodCountryOfOrigin'])
    '3rd Product info'
    #can.drawString(54, 618, dataProductsInfo['prodDescription'])
    #can.drawString(204, 618, dataProductsInfo['prodQuantity'])
    #can.drawString(250, 618, dataProductsInfo['prodWeight'])
    #can.drawString(320, 618, dataProductsInfo['prodValue'])
    #can.drawString(370, 618, dataProductsInfo['prodHSTarif'])
    #can.drawString(470, 618, dataProductsInfo['prodCountryOfOrigin'])
    '4th Product info'
    #can.drawString(54, 618, dataProductsInfo['prodDescription'])
    #can.drawString(204, 618, dataProductsInfo['prodQuantity'])
    #can.drawString(250, 618, dataProductsInfo['prodWeight'])
    #can.drawString(320, 618, dataProductsInfo['prodValue'])
    #can.drawString(370, 618, dataProductsInfo['prodHSTarif'])
    #can.drawString(470, 618, dataProductsInfo['prodCountryOfOrigin'])
    
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
    outputStream = open(CN23_OutPath + '/' + userEmail + '/' + MarketPlaceId + '-' + cn23_idx + "-CN23.pdf", "wb")
    output.write(outputStream)
    outputStream.close()

    'Clear UserUploads and CN23Out Folders'
    UserUploadPath = ParentPath + '/' + userEmail + '/'
    clearFolderData(UserUploadPath)
    cn23Path = CN23_OutPath + '/' + userEmail + '/'
    clearFolderData(cn23Path)

def clearFolderData(mypath):
    for root, dirs, files in os.walk(mypath):
        for file in files:
            os.remove(os.path.join(root, file))

def sendGridEmail():

    client = sendgrid.SendGridClient("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")
    message = sendgrid.Mail()

    message.add_to("gekko1990@gmail.com")
    message.set_from("gekko1990@gmail.com")
    message.set_subject('CN23')
    message.set_html("Click the Link to download the CN23 PDFs! : " + 'https://s21.q4cdn.com/374334112/files/doc_downloads/test.pdf')

    client.send(message)

#if __name__ == '__main__':
#    app.run(debug=True, port=2000)

#fetchWixData('50d16d4b6a84952cd160c461b4aafd92409427cdf47d17c89c004f3c0cf332426ef75ca954115ef6b4ca79a7f9e694911e60994d53964e647acf431e4f798bcd5df106f0a689304605995f23566f925e02c1cb1fbfd9d63a2968755a2cf81e5d')
#fetchWixData('bf03dd816bf20d2dec142f9ba4e9cec682908a42145b0d17c57cc89498ca8770ec760030e230d62a29cf0b1c305a52861e60994d53964e647acf431e4f798bcd75fe9676af4e71b77777835b55c1c543ba2d300f6325b6d634ee736961ec9c5f')
#sendGridEmail()


