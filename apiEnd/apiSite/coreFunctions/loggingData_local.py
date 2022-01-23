from os import remove
import csv
from datetime import datetime
from apiSite.cores import config


def logCashTransaction(cur, userID, cashVolume, direction):
    getUserName = "SELECT username FROM users WHERE userID = '"+str(userID)+"';"
    basePath = "C:/Users/alico/OneDrive/Documents/MCInvest/placeHolder/priceMoves/"
    filePath = basePath + "cashTransactions.csv"
    cur.execute(getUserName)
    userName = cur.fetchone()[0]
    if direction == "withdrawal":
        sendingDirection = "User Withdrawal"
    elif direction == "deposit":
        sendingDirection = "User Deposit"
    elif direction == "outOfUser":
        sendingDirection = "Exchange-to-User Transfer"
    elif direction == "intoUser":
        sendingDirection = "User-to-Exchange Transfer"
    currentTime = datetime.now()
    timeString = currentTime.strftime("%Y-%m-%d %H:%M:%S")
    with open(filePath, "a") as csvfile:
        writerJob = csv.writer(csvfile, lineterminator='\n')
        writerJob.writerow([timeString, userName, sendingDirection, str(cashVolume)])


def logTrades(cur, ticker):
    basePath = "C:/Users/alico/OneDrive/Documents/MCInvest/placeHolder/logs/tradelogs"
    filePath = basePath + "cashTransactions.csv"
    fetchingCloseTrades = "SELECT closedTrades.tradeID, users.username, closedTrades.tradeType, closedTrades.quantStock, closedTrades.stockPrice FROM users, closedTrades WHERE closedTrades.userID = users.userID AND ticker = '"+ticker+"';"
    fetchingOpenTrades = "SELECT openTrades.tradeID, users.username, openTrades.tradeType, openTrades.quantStock, openTrades.stockPrice FROM users, openTrades WHERE openTrades.userID = users.userID AND ticker = '"+ticker+"';"
    print(fetchingOpenTrades)
    cur.execute(fetchingCloseTrades)
    allClosedTrades = cur.fetchall()
    cur.execute(fetchingOpenTrades)
    allOpenTrades = cur.fetchall()
    filePath = basePath + "/logs/tradelogs/" + ticker + ".csv"
    with open(filePath, "w+") as csvfile:
        writerJob = csv.writer(csvfile, lineterminator='\n')
        writerJob.writerow(["Trade ID", "Username", "Trade Type", "Quantity of Stock", "Stock Price", "Status"])
        for trade in allOpenTrades:
            trade = list(trade)
            trade.append("Open")
            writerJob.writerow(trade)
        for trade in allClosedTrades:
            trade = list(trade)
            trade.append("Closed")
            writerJob.writerow(trade)


def logPriceUpdate(ticker, newPrice):
    currentTime = datetime.now()
    timeString = currentTime.strftime("%Y-%m-%d %H:%M:%S")
    basePath = "C:/Users/alico/OneDrive/Documents/MCInvest/placeHolder/"
    filePath = basePath + "priceMoves/" + ticker + ".csv"
    with open(filePath, "a") as csvfile:
        writerJob = csv.writer(csvfile, lineterminator='\n')
        writerJob.writerow([timeString, newPrice])


def logAllPrices():
    fetchingQuery = "SELECT stockticker, stockprice FROM stocks;"
    conn = config()
    with conn.cursor() as cur:
        cur.execute(fetchingQuery)
        stocksToUpdate = cur.fetchall()
    for stock in stocksToUpdate:
        logPriceUpdate(stock[0], stock[1])
