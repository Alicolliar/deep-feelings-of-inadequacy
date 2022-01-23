from flask import Blueprint, request
from apiSite.coreFunctions import gettingData_local as gettingData
from json import dumps

bp = Blueprint('private', __name__)


@bp.route('/getstock/', methods=['GET', 'POST'])
def sendStockData():
    if type(request) is 'NoneType':
        return dumps({"error": "Incorrect data type"})
    requestTicker = request.get_json()["ticker"]
    try:
        apiKey = request.get_json()["authentication"]
        keyVal = gettingData.keyValid(apiKey)
    except:
        keyVal = False
    if not keyVal:
        return dumps({"unauthenticated":"You do not have a valid apikey"}, indent=(4))
    quickCheck = gettingData.checkTicker(requestTicker)
    if not quickCheck:
        return dumps({"error":"No such ticker"})
    sentData = gettingData.getStockInfo(requestTicker)
    return dumps(sentData, indent=(4))

@bp.route('/getPastPrices/', methods=['POST'])
def pastPrices():
    """Returns the last 5 price points without datetimes"""
    requestTicker = request.get_json()["ticker"]
    try:
        apiKey = request.get_json()["authentication"]
        keyVal = gettingData.keyValid(apiKey)
    except:
        keyVal = False
    if not keyVal:
        return dumps({"unauthenticated":"You do not have a valid apikey"}, indent=(4))
    quickCheck = gettingData.checkTicker(requestTicker)
    if not quickCheck:
        return dumps({"error":"No such ticker"}, indent=(4))
    useless, pastPrices = gettingData.getStockInfo(requestTicker)
    sendingJSON = {
        "ticker": requestTicker,
        pastPrices: pastPrices[::-1]
    }
    return dumps(sendingJSON, indent=(4))
