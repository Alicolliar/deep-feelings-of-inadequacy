from mainSite.cores import config
from flask import current_app
import csv
from os import remove


def getStockInfo(ticker):
    conn = config()
    with conn.cursor() as cur:
        query = "SELECT regionname, stockPrice, stockVolume, stockMarketCap FROM stocks WHERE stockticker = '"+ticker+"';"
        print(query)
        try:
            cur.execute(query)
            queriedArray = cur.fetchone()
        except:
            return "HCF-DBE"
        if len(queriedArray) < 1:
            return "HCF-NE"
        keys = ["name", "price", "volume", "marketcap"]
        returningData = {k: v for k, v in zip(keys, queriedArray)}
    return returningData


def getMarketPrice(ticker):
    conn = config()
    with conn.cursor() as cur:
        query = "SELECT stockPrice FROM stocks WHERE stockticker = '"+ticker+"';"
        cur.execute(query)
        return int(cur.fetchone()[0])


def getTickers():
    conn = config()
    with conn.cursor() as cur:
        query = "SELECT stockticker FROM stocks;"
        cur.execute(query)
        queriedArray = cur.fetchall()
        print(queriedArray)
    returnAbleArray = []
    for stock in queriedArray:
        returnAbleArray.append(stock[0])
    return returnAbleArray


def getPastPrices(ticker):
    basePath = "C:/Users/alico/OneDrive/Documents/MCInvest/placeHolder/priceMoves/"
    filePath = basePath + ticker + ".csv"
    with open(filePath, "r") as csvfile:
        dateTimes = []
        prices = []
        priceReader = csv.reader(csvfile)
        next(priceReader)
        for priceCombo in priceReader:
            dateTimes.append(priceCombo[0])
            prices.append(priceCombo[1])
    return dateTimes, prices


def getAllTickers():
    query = "SELECT stockticker FROM stocks;"
    conn = config()
    with conn.cursor() as cur:
        cur.execute(query)
        tickers = cur.fetchall()
    nicerList = []
    for tickArr in tickers:
        nicerList.append(tickArr[0])
    return nicerList


def checkCashValue(cur, userID, request):
    receivalQuery = "SELECT cashBalance FROM users WHERE userID = "+str(userID)+";"
    cur.execute(receivalQuery)
    userBal = cur.fetchone()[0]
    if userBal > request:
        return True
    else:
        return False


def checkPortValue(cur, userID, stock, quant):
    receivalQuery = "SELECT volumeOwned FROM stockHoldings WHERE stockholder = "+str(userID)+" AND stockticker = '"+stock+"';"
    cur.execute(receivalQuery)
    quantityOwned = cur.fetchone()
    if len(quantityOwned) < 1:
        return "You don't hold any of this stock"
    difference = quantityOwned[0] - quant
    if difference >= 0:
        return None
    else:
        return "You don't hold enough of this stock"

def getOpenOrders(cur, stock):
    grabQuery = "SELECT tradeType, quantStock, stockPrice, totalTradeValue FROM openTrades WHERE ticker = '"+ticker+"';"
    cur.execute(grabQuery)
    openOrders = cur.fetchall()
    return openOrders