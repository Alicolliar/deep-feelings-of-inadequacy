from mainSite.coreFunctions import loggingData as loggingData


def cashDeposit(cur, user, cashToDeposit):
    cashCheckQueryUser = "SELECT cashBalance FROM users WHERE userID = '"+str(user)+"';"
    cur.execute(cashCheckQueryUser)
    currentBalance = cur.fetchone()[0]
    if currentBalance == 0:
        newBalance = cashToDeposit
    else:
        newBalance = cashToDeposit + currentBalance
    loggingData.logCashTransaction(cur, user, cashToDeposit, "deposit")
    cashDepositQuery = "UPDATE users SET cashBalance = '"+str(newBalance)+"' WHERE userID = '"+str(user)+"';"
    cur.execute(cashDepositQuery)


def cashWithdrawal(cur, user, cashToWithdraw):
    cashCheckQueryUser = "SELECT cashBalance FROM users WHERE userID = '"+str(user)+"';"
    cur.execute(cashCheckQueryUser)
    currentBalance = cur.fetchone()[0]
    if currentBalance == 0:
        return "HCF-OUC"
    else:
        newBalance = currentBalance - cashToWithdraw
    cashDepositQuery = "UPDATE users SET cashBalance = '"+str(newBalance)+"' WHERE userID = '"+str(user)+"';"
    loggingData.logCashTransaction(cur, user, cashToWithdraw, "withdrawal")
    cur.execute(cashDepositQuery)
    return "Success"


def ExchangeCashTransfer(cur, userID, cashToTransfer, direction):
    userBalanceCheck = "SELECT cashBalance FROM users WHERE userID = '"+str(userID)+"';"
    exchangeBalanceCheck = "SELECT cashBalance FROM users WHERE userID = '2';" # NOTE: This ID should be changed to that of the exchange account, on my test DB it was 2
    cur.execute(userBalanceCheck)
    userBalance = cur.fetchone()[0]
    cur.execute(exchangeBalanceCheck)
    exchangeBalance = cur.fetchone()[0]
    if direction == "outOfUser":
        newUserBalance = userBalance - cashToTransfer
        newExchangeBalance = exchangeBalance + cashToTransfer
        if newUserBalance < 0:
            return "HCF-UOC"
        userBalanceAddition = "UPDATE users SET cashBalance = '"+str(newUserBalance)+"' WHERE userID = '"+str(userID)+"';"
        exchangeBalanceSubtraction = "UPDATE users SET cashBalance = '"+str(newExchangeBalance)+"' WHERE userID = '2';" # NOTE: The userID here should be adjusted to that of the exchange user
        cur.execute(userBalanceAddition)
        cur.execute(exchangeBalanceSubtraction)
    elif direction == "intoUser":
        newUserBalance = userBalance + cashToTransfer
        newExchangeBalance = exchangeBalance - cashToTransfer
        userBalanceAddition = "UPDATE users SET cashBalance = '"+str(newUserBalance)+"' WHERE userID = '"+str(userID)+"';"
        exchangeBalanceSubtraction = "UPDATE users SET cashBalance = '"+str(newExchangeBalance)+"' WHERE userID = '2';" # NOTE: The userID here should be adjusted to that of the exchange user
        cur.execute(userBalanceAddition)
        cur.execute(exchangeBalanceSubtraction)
    loggingData.logCashTransaction(cur, userID, cashToTransfer, direction)
    return "Success"
