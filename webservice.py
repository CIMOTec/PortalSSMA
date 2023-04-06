import requests
from bs4 import BeautifulSoup
import lxml

pass_url = "https://inteligencia.conbras.com/Prisma4/WebServices/Public/ExportData.asmx"
pass_headers = {'content-type': 'text/xml'}

pass_body = f"""<?xml version="1.0" encoding="utf-8"?>
                <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                <soap:Body>
                    <ExportQueryData xmlns="http://sisteplant.com/">
                        <company>MRVVT-ID02</company>
                        <user>236325</user>
                        <query>Q_Web_01</query>
                            <parameterList>
                                <QueryParameters>
                                <ParamName>requester</ParamName>
                                <ParamValue>236325</ParamValue>
                                </QueryParameters>
                            </parameterList>
                    </ExportQueryData>
                </soap:Body>
                </soap:Envelope>"""

response = requests.post(pass_url, data=pass_body, headers=pass_headers)
soup = BeautifulSoup(response.text, 'xml')
print(soup.costCenterClient.text)

f = open("sla.xml", "w")
f.write(str(soup))
f.close()
