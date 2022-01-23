from flask import Blueprint, request
from apiSite.coreFunctions import gettingData_local as gettingData
from json import dumps

bp = Blueprint('public', __name__)


@bp.route('/getstock/', methods=['POST'])
def getStockData():
    requestTicker = request.get_json()
    quickCheck = gettingData.checkTicker(requestTicker)
    if not quickCheck:
        return dumps({"error":"No such ticker"}, indent=(4))
    sentData = gettingData.getStockInfo(requestTicker)
    return dumps(sentData, indent=(4))

@bp.route('/getPastPrices/', methods=['POST'])
def pastPrices():
    """Returns the last 5 price points without datetimes"""
    requestTicker = request.get_json()["ticker"]
    quickCheck = gettingData.checkTicker(requestTicker)
    if not quickCheck:
        return dumps({"error":"No such ticker"}, indent=(4))
    useless, pastPrices = gettingData.getStockInfo(requestTicker)
    sendingJSON = {
        "ticker": requestTicker,
        pastPrices: pastPrices[-5:-1:-1]
    }
    return dumps(sendingJSON, indent=(4))
