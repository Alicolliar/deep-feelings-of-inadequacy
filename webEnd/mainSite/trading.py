from mainSite.coreFunctions import tradeExecution, gettingData as gettingData
from flask import Blueprint, render_template, request, session, url_for, redirect
from mainSite.cores import config

bp = Blueprint('trades', __name__)


@bp.route('/tradeEntry', methods=['GET', 'POST'])
def tradeEntry():
    if 'user' not in session:
        return redirect(url_for("userRelated.loginPage"))
    if request.method == 'POST':
        formData = request.form
        ticker = formData["ticker"]
        quant = formData["quantity"]
        priceSelect = formData["priceSelect"]
        tradeType = formData["tradeType"]
        existingTickers = gettingData.getTickers()
        if ticker not in existingTickers:
            return render_template("stockPages/tradepage.html", errorMessage="This ticker does not exist")
        if priceSelect == "market":
            price = gettingData.getMarketPrice(ticker)
        elif priceSelect == "own":
            price = formData["priceSet"]
        else:
            return render_template("stockPages/tradepage.html", errorMessage="Price setter does not exist")
        return redirect(url_for("trades.tradeConfirm", ticker=ticker, quant=quant, price=price, tradeType=tradeType))
    return render_template("stockPages/tradepage.html")


@bp.route('/tradeConfirm/<ticker>/<quant>/<price>/<tradeType>', methods=["GET", "post"])
def tradeConfirm(ticker, quant, price, tradeType):
    conn = config()
    if 'user' not in session:
        return redirect(url_for("userRelated.loginPage"))
    totalValue = float(price) * float(quant)
    data = [ticker, quant, price, tradeType, totalValue]
    if request.method == 'POST':
        stockInfo = gettingData.getStockInfo(ticker)
        submitter = session['user']
        if isinstance(stockInfo, int):
            print(stockInfo)
            return redirect(url_for("error.tradeError"))
        else:
            with conn.cursor() as cur:
                possibleError = tradeExecution.tradeSubmit(cur, tradeType, ticker, quant, price, submitter)
                if possibleError:
                    return render_template("stockPages/tradeConfirm.html", data=data, errMess=possibleError)
                conn.commit()
                return redirect(url_for("view.portfolioView"))

    return render_template("stockPages/tradeConfirm.html", data=data)
