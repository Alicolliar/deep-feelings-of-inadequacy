from flask import Blueprint, render_template, request, session, redirect, url_for, current_app as appConf
from mainSite.cores import config
from mainSite.coreFunctions import cashTransactions, gettingData as gettingData, tradeExecution
from google.cloud import storage
from csv import writer
from os import remove
client = storage.Client()
bucket = client.get_bucket('nsinvest-infra.appspot.com')

bp = Blueprint('admin', __name__)


@bp.route('/users', methods=['GET', 'POST'])
def adminUser():
    conn = config()
    if not session['admin']:
        return redirect("userRelated.login")
    if request.method == "POST":
        formData = request.form
        if "upgrdaeUser" in formData:
            userToUpgrade = formData["userName"]
            getUserQuery = "SELECT userID, adminStatus FROM users WHERE username = '"+userToUpgrade+"';"
            with conn.cursor() as cur:
                cur.execute(getUserQuery)
                usersWithName = cur.fetchall()
                if len(usersWithName) != 1:
                    return render_template("admin/userAdmin.html", errorThing="The username is likely incorrect, honestly, get a fucking education you motherfucking casual")
                activeUser = usersWithName[0]
                if activeUser[1] == "True":
                    return render_template("admin/userAdmin.html", errorThing="The user is already an administrator, how could not notice you absolute fucktard")
                updateAdminStatus = "UPDATE users SET adminStatus = 'True' WHERE userID = '"+str(activeUser[0])+"';"
                cur.execute(updateAdminStatus)
                return render_template("admin/adminUser.html", successThing="User updated to admin")
        elif "userTransference" in formData:
            direction = formData["cashDirection"]
            value = float(formData["cashToTransfer"])
            userToUpgrade = formData["userName"]
            getUserQuery = "SELECT userID FROM users WHERE username = '"+userToUpgrade+"';"
            with conn.cursor() as cur:
                cur.execute(getUserQuery)
                usersWithName = cur.fetchall()
                if len(usersWithName) != 1:
                    return render_template("admin/userAdmin.html", errorThing="The username is likely incorrect, honestly, get a fucking education you motherfucking casual")
                activeUser = usersWithName[0]
                if direction == "deposit":
                    returnFromData = cashTransactions.cashDeposit(cur, activeUser[0], value)
                elif direction == "withdrawal":
                    returnFromData = cashTransactions.cashWithdrawal(cur, activeUser[0], value)
                if returnFromData:
                    if returnFromData[0:3] == "HCF":
                        return render_template("admin/userAdmin.html", errorThing="An error occurred in the transaction <b>AND IT'S ALL YOUR FAULT YOU CUNT</b>")
                return render_template("admin/userAdmin.html", successThing="All clear")
        elif "deleteUser" in formData:
            userName = formData["userName"]
            userConfirm = "SELECT userID, cashBalance FROM users WHERE username = '"+str(userName)+"';"
            with conn.cursor() as cur:
                cur.execute(userConfirm)
                allUsers = cur.fetchall()
                if len(allUsers) != 1:
                    return render_template("admin/userAdmin.html", errorThing="No such user, you thick piece of shit")
                userID = allUsers[0]
                userCash = allUsers[1]
                if userCash >= 0:
                    getExchangeBalQuery = "SELECT userbalance FROM users WHERE username = 'Exchange';"
                    cur.execute(getExchangeBalQuery)
                    currentExBal = cur.fetchone()
                    newExchangeBalance = userCash + currentExBal[0]
                    transferExchangeCash = "UPDATE users SET userBalance = "+str(newExchangeBalance)+" WHERE username = 'Exchange';"
                    cur.execute(transferExchangeCash)
                deletionQuery = "DELETE FROM users WHERE userID = '"+str(userID)+"';"
                cur.execute(deletionQuery)
                conn.commit()
                return render_template("admin/userAdmin.html", successThing="User removed")
        elif "keyIssue" in formData:
            userName = formData["userName"]
            newKey = formData["newKey"]
            userConfirm = "SELECT userID FROM users WHERE username = '"+str(userName)+"';"
            with conn.cursor() as cur:
                cur.execute(userConfirm)
                allUsers = cur.fetchone()
                if len(allUsers) != 1:
                    return render_template("admin/userAdmin.html", errorThing="No such user, you thick piece of shit")
                userID = allUsers[0]
                additionQuery = "INSERT INTO apikeys (accID, apikey, revoked) VALUES ("+str(userID)+", '"+newKey+"', false);"
                cur.execute(additionQuery)
                conn.commit()
            successThing="Api Key "+newKey+" added for user"
            return render_template("admin/userAdmin.html", successThing=successThing)
    return render_template("admin/userAdmin.html")


@bp.route('/stocks', methods=['GET', 'POST'])
def adminStocks():
    conn = config()
    if not session['admin']:
        return redirect(url_for("userRelated.login"))
    if request.method == "POST":
        formData = request.form
        if "addStock" in formData:
            companyName = formData["comName"]
            ticker = formData["stockTicker"]
            ticker = ticker.upper()
            vol = float(formData["volume"])
            marketCap = float(formData["marketCap"])
            startPrice = marketCap/vol
            userName = formData["startingUser"]
            userQuery = "SELECT userID FROM users WHERE username = '"+userName+"';"
            addStockQuery = "INSERT INTO stocks (stockTicker, regionname, stockPrice, stockVolume, stockMarketCap) VALUES ('"+ticker+"', '"+companyName+"', '"+str(startPrice)+"', '"+str(int(vol))+"', '"+str(marketCap)+"');"
            allTickers = gettingData.getAllTickers()
            if ticker in allTickers:
                return render_template("admin/stocksAdmin.html", errorThing="That ticker already exists, you knitted scarf, you FUCKING OMNISHAMBLES")
            basePath = appConf.config["STORED_DATA_PATH"] + "/priceMoves/"
            filePath = basePath + ticker + ".csv"
            tmpFilePath = "/tmp/"+ticker+".csv"
            with open(tmpFilePath, "w") as tmpFile:
                writerJob = writer(tmpFile, lineterminator='\n')
                writerJob.writerow(["Timestamp", "Price"])
            blob = bucket.blob(filePath)
            blob.upload_from_filename(tmpFilePath)
            with conn.cursor() as cur:
                cur.execute(userQuery)
                user = cur.fetchone()
                if len(user) < 1:
                    return render_template("admin/stocksAdmin.html", errorThing="The user does not exist, you fucking pillock")
                user = user[0]
                cur.execute(addStockQuery)
                addHoldingQuery = "INSERT INTO stockHoldings (stockTicker, stockHolder, volumeOwned, purchasePrice, totalValue) VALUES ('"+ticker+"', '"+str(user)+"', '"+str(int(vol))+"', '"+str(startPrice)+"', '"+str(vol*startPrice)+"');"
                conn.commit()
                cur.execute(addHoldingQuery)
                conn.commit()
            retString = ticker + " added to exchange, awaiting release"
            remove(tmpFilePath)
            return render_template("admin/stocksAdmin.html", successThing=retString)
        elif "manualSale" in formData:
            ticker = formData["ticker"]
            userName = formData["userName"]
            tradeType = formData["tradeType"]
            quant = formData["quantity"]
            price = gettingData.getMarketPrice(ticker)
            userQuery = "SELECT userID FROM users WHERE username = '"+userName+"';"
            with conn.cursor() as cur:
                cur.execute(userQuery)
                user = cur.fetchone()
                if len(user) < 1:
                    return render_template("admin/stocksAdmin.html", errorThing="The user does not exist, you fucking pillock")
                user = user[0]
                tradeExecution.tradeSubmit(cur, tradeType, ticker, quant, price, user, True)
                conn.commit()
            return render_template("admin/stocksAdmin.html", successThing="Sale Entered")
    return render_template("admin/stocksAdmin.html")


@bp.route('/compliance')
def adminCompliance():
    if not session['admin']:
        return redirect(url_for("userRelated.login"))
    tickers = gettingData.getAllTickers()
    return render_template("admin/complianceAdmin.html", tickers=tickers)
