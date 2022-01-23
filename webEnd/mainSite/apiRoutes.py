from mainSite.coreFunctions import loggingData as loggingData
from flask import Blueprint
bp = Blueprint('privateApi', __name__)

@bp.route('/logPrices', methods=['GET'])
def logPriceWorkaround():
    loggingData.logAllPrices()
    return '1'
