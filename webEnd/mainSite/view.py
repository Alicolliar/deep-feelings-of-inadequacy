from flask import Blueprint, render_template, redirect, url_for, session
from mainSite.coreFunctions import gettingData as gettingData
from mainSite.cores import config

bp = Blueprint('view', __name__)


@bp.route('/allstocks')
def viewAllStocks():
    grabQuery = """SELECT stockticker, regionName, stockPrice, stockMarketCap, stockVolume
                   FROM stocks;"""
    conn = config()
    with conn.cursor() as cur:
        cur.execute(grabQuery)
        receivedData = cur.fetchall()
    return render_template("views/allStocks.html", allStocks=receivedData)


@bp.route('/stock/<ticker>')
def viewCertainStock(ticker):
    baseData = gettingData.getStockInfo(ticker)
    timepoints, prices = gettingData.getPastPrices(ticker)
    baseData["ticker"] = ticker
    return render_template("views/stockView.html", baseData=baseData, timepoints=timepoints, prices=prices)


@bp.route('/orderBook')
def orderBookView():
    grabQuery = "SELECT tradeopened, ticker, tradeType, stockPrice, quantStock, totalTradeValue, stockRemaining FROM openTrades ORDER BY tradeopened ASC;"
    conn = config()
    with conn.cursor() as cur:
        cur.execute(grabQuery)
        openOrders = cur.fetchall()
    return render_template("views/orderBook.html", allStocks=openOrders)


@bp.route('/portfolioView')
def portfolioView():
    if 'user' not in session:
        return redirect(url_for("userRelated.loginPage"))
    conn = config()
    userID = session['user']
    findHoldingsQuery = """SELECT stockticker, volumeowned, purchaseprice, totalvalue
                           FROM stockholdings
                           WHERE stockholder = """+str(userID)+""";"""
    userCashQuery = """SELECT cashbalance
                       FROM users
                       WHERE userID = """+str(userID)+""";"""
    userTradesQuery = """SELECT ticker, tradeType, quantStock, stockPrice
                         FROM closedTrades
                        WHERE userID = """+str(userID)+""";"""
    with conn.cursor() as cur:
        cur.execute(findHoldingsQuery)
        holdings = cur.fetchall()
        cur.execute(userCashQuery)
        userCash = cur.fetchone()[0]
        cur.execute(userTradesQuery)
        userTrades = cur.fetchall()
    holdingPass = []
    totalValue = userCash
    for holding in holdings:
        holding = list(holding)
        currentPrice = gettingData.getMarketPrice(holding[0])
        holding.append(currentPrice)
        holdingPass.append(holding)
        assetValue = currentPrice * holding[1]
        totalValue += assetValue
    print(holdingPass)
    return render_template("views/portfolioView.html", assets=holdingPass, totalValue=totalValue, cashBal=userCash, trades=userTrades)
