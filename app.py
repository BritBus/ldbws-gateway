import zeep
import os
from flask import Flask, jsonify, Response

app = Flask(__name__)

token = os.environ['BRITBUS_LDBWS_TOKEN']

wsdl = 'https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx?ver=2021-11-01'
client = zeep.Client(wsdl=wsdl)

auth_header = zeep.xsd.Element(
  '{http://thalesgroup.com/RTTI/2013-11-28/Token/types}AccessToken',
  zeep.xsd.ComplexType([
      zeep.xsd.Element(
          '{}TokenValue',
          zeep.xsd.String()),
  ])
)
auth_header_value = auth_header(TokenValue=token)

@app.route('/departures/<crs>')
def departures(crs):
  with client.settings(raw_response=True):
    ldbwsReply = client.service.GetDepBoardWithDetails(
      numRows=10, 
      crs=crs,
      timeOffset=0, 
      timeWindow=119, 
      _soapheaders=[auth_header_value]
    )

    # replyDict = xmltodict.parse(ldbwsReply.text)
    # response = jsonify(replyDict)
    # response.headers.add('Access-Control-Allow-Origin', '*')
    # return response
    return Response(ldbwsReply.text, mimetype='text/xml')

@app.route('/service/<serviceid>')
def service(serviceid):
  with client.settings(raw_response=True):
    ldbwsReply = client.service.GetServiceDetails(
      serviceID=serviceid,
      _soapheaders=[auth_header_value]
    )

    return Response(ldbwsReply.text, mimetype='text/xml')