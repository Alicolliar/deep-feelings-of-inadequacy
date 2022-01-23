from mainSite.coreFunctions import cashTransactions, gettingData


def tradeSubmit(cur, tradeType, ticker, volume, price, userSubmitting, manual=False):
    """
    Function needs to enter and match trades
    Inputs
        cur - A database cursor  bject
        tradeType - The type of trade, either "Buy" or "Sell"
        ticker - The exchange traded ticker that the trade is for
        price - The price being traded at
        userSubmitting - The userID of the user entering the trade
    Processes
        Stock price adjusted
        Any trade matches completed
        Trade entered
    Outputs
        In the event of an error, a HCF is needed, otherwise no error
    """
    volume = float(volume)
    price = float(price)
    totalValue = volume * price
    if not manual:
        stockPriceAdjustment(cur, tradeType, ticker, volume, price)
    matchingTrades = findMatches(cur, ticker, tradeType, price)
    if len(matchingTrades) < 1:
        tradeAddQuery = """INSERT INTO openTrades
        (userID, tradeType, ticker, quantStock, stockPrice, totalTradeValue, tradeOpened, stockRemaining)
        VALUES ('"""+str(userSubmitting)+"""', '"""+tradeType+"""', '"""+ticker+"""', """+str(int(volume))+""", """+str(price)+""", """+str(totalValue)+""", NOW(), """+str(volume)+""");"""
        cur.execute(tradeAddQuery)
        return
    remainingVolume = volume
    for trade in matchingTrades:
        if remainingVolume == 0:
            break
        remainingVolume = tradeMatchSubmissions(cur, trade, remainingVolume)

    if remainingVolume > 0:
        tradeAddQuery = """INSERT INTO openTrades
                           (userID, tradeType, ticker, quantStock, stockPrice, totalTradeValue, tradeOpened, stockRemaining) VALUES
                           ('"""+str(userSubmitting)+"""', '"""+tradeType+"""', '"""+ticker+"""', """+str(volume)+""", """+str(price)+""", """+str(totalValue)+""", NOW(), """+str(remainingVolume)+""");"""
    elif remainingVolume == 0:
        if tradeType == "Buy":
            cashDirection = "outOfUser"
        elif tradeType == "Sell":
            cashDirection = "intoUser"
        tradeAddQuery = """INSERT INTO closedTrades
                           (userID, tradeType, ticker, quantStock, stockPrice,  tradeClosed)
                           VALUES ('"""+str(userSubmitting)+"""', '"""+tradeType+"""', '"""+ticker+"""', """+str(int(volume))+""", """+str(round(price,2))+""", NOW());"""
        cashTransactions.ExchangeCashTransfer(cur, userSubmitting, totalValue, cashDirection)
    cur.execute(tradeAddQuery)


def findMatches(cur, ticker, tradeType, price):
    priceUpper = 1.05*price
    priceLower = 0.95*price
    if tradeType == "Buy":
        opposingType = "Sell"
    elif tradeType == "Sell":
        opposingType = "Buy"
    findQuery = """SELECT tradeID, stockRemaining
                   FROM openTrades
                   WHERE ticker = '"""+ticker+"""' AND tradeType = '"""+opposingType+"""' AND stockPrice BETWEEN """+str(round(priceLower,2))+""" AND """+str(round(priceUpper,2))+""" ORDER BY tradeopened DESC;"""
    print(findQuery)
    cur.execute(findQuery)
    return cur.fetchall()


def stockPriceAdjustment(cur, tradeType, ticker, volume, price):
    stockData = gettingData.getStockInfo(ticker)
    currentPrice = float(stockData["price"])
    wholeStockVolume = float(stockData["volume"])
    volWeight = volume/wholeStockVolume
    if tradeType == "Buy":
        priceAdjust = 1+((price-currentPrice)/currentPrice)
        newPrice = currentPrice * (1+(priceAdjust*volWeight))
    elif tradeType == "Sell":
        priceAdjust = 1-((price-currentPrice)/currentPrice)
        newPrice = currentPrice * (1-(priceAdjust*float(volWeight)))
    updateQuery = """UPDATE stocks
                     SET stockPrice = """+str(newPrice)+"""
                     WHERE stockTicker = '"""+ticker+"""';"""
    cur.execute(updateQuery)


def tradeMatchSubmissions(cur, workingTrade, remainingVolume):
    workingID = workingTrade[0]
    workingVol = workingTrade[1]
    volumeDifference = remainingVolume - workingVol
    if volumeDifference >= 0:
        closeOrder(cur, workingID)
    elif volumeDifference < 0:
        newWorkingVolume = workingVol - remainingVolume
        volumeDifference = 0
        updateWorkerVolQuery = """UPDATE openTrades
                                SET stockRemaining = """+str(newWorkingVolume)+"""
                                WHERE tradeID = '"""+str(workingID)+"""';"""
        cur.execute(updateWorkerVolQuery)
    return volumeDifference


def closeOrder(cur, orderID):
    selectTrade = """SELECT ticker, quantStock, tradeType, userID, stockPrice
                     FROM openTrades
                     WHERE tradeID = '"""+str(orderID)+"""';"""
    removeTrade = """DELETE FROM openTrades
                   WHERE tradeID = '"""+str(orderID)+"""';"""
    cur.execute(selectTrade)
    selectedTrade = cur.fetchone()
    tradeUser = selectedTrade[3]
    tradeTicker = selectedTrade[0]
    tradeQuant = selectedTrade[1]
    tradeType = selectedTrade[2]
    tradePrice = selectedTrade[4]
    tradeValue = tradeQuant * tradePrice
    if tradeType == "Buy":
        cashDirection = "outOfUser"
    elif tradeType == "Sell":
        cashDirection = "intoUser"
    tradeEntry = """INSERT INTO closedTrades
                    (userID, tradeType, ticker, quantStock, stockPrice,  tradeClosed)
                    VALUES ('"""+str(tradeUser)+"""', '"""+tradeType+"""', '"""+tradeTicker+"""', '"""+str(tradeQuant)+"""', '"""+str(tradePrice)+"""', NOW());"""
    cur.execute(tradeEntry)
    cur.execute(removeTrade)
    portfolioAdjustments(cur, tradeUser, tradeTicker, tradeQuant, tradePrice, tradeType)
    cashCheck = cashTransactions.ExchangeCashTransfer(cur, tradeUser, tradeValue, cashDirection)
    if cashCheck[0:3] == "HCF":
        return cashCheck


def portfolioAdjustments(cur, user, ticker, volume, price, tradeType):
    user = str(user)
    oldDataQuery = """SELECT volumeOwned, purchasePrice
                      FROM stockholdings
                      WHERE stockTicker = '"""+ticker+"""'
                      AND stockholder = """+user+""";"""
    cur.execute(oldDataQuery)
    currentHolding = cur.fetchone()
    if len(currentHolding) < 1:
        avgPurchasePrice = price
        newVolume = volume
        totalValue = avgPurchasePrice * newVolume
        updatePortQuery = """INSERT INTO stockholdings
                           (stockTicker, stockholder, volumeOwned, purchasePrice, totalValue)
                           VALUES ('"+ticker+"', '"+user+"', "+str(int(volume))+", "+avgPurchasePrice+", "+totalValue+");"""
    else:
        if tradeType == "Buy":
            newVolume = currentHolding[0] + volume
            avgPurchasePrice = ((volume * price)+(currentHolding[0]*currentHolding[1])/newVolume)
        elif tradeType == "Sell":
            newVolume = currentHolding[0] - volume
            avgPurchasePrice = currentHolding[1]
        totalValue = avgPurchasePrice * newVolume
        updatePortQuery = "UPDATE stockholdings SET volumeOwned = '"+str(newVolume)+"', purchasePrice = "+str(round(avgPurchasePrice, 2))+", totalValue = "+str(round(totalValue, 2))+" WHERE stockTicker = '"+ticker+"' AND stockholder = '"+user+"';"
    cur.execute(updatePortQuery)
