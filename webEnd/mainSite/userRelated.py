from flask import Blueprint, render_template, request, session, redirect, url_for
from mainSite.cores import config, passEncryption
from psycopg2 import Binary
bp = Blueprint('userRelated', __name__)


@bp.route('/signUp', methods=['GET', 'POST'])
def userRegistration():
    conn = config()
    if 'user' in session:
        return redirect(request.referrer)
    if request.method == "POST":
        allData = request.form
        userName = str(allData["userName"])
        pWord = allData["pWord"]
        passConfirm = allData["pWordConf"]
        if pWord != passConfirm:
            return render_template("userRelatedItems/userSignUp.html", errMessage="Password's don't match, please try again")
        passEncrypted = passEncryption(pWord)
        with conn.cursor() as cur:
            userCheckQuery = "SELECT COUNT(userid) FROM users WHERE username = '" + userName+"';"
            cur.execute(userCheckQuery)
            userNameCount = cur.fetchone()
            if int(userNameCount[0]) != 0:
                return render_template("userRelatedItems/userSignUp.html", errMessage="Username already taken")
            userQuery = "INSERT INTO users(username, passwordhash, cashBalance) VALUES ('" + \
                userName+"', '"+passEncrypted+"', 0)"
            cur.execute(userQuery)
            conn.commit()
            conn.close()
    return render_template("userRelatedItems/userSignUp.html")


@bp.route('/login', methods=["GET", "POST"])
def loginPage():
    conn = config()
    if 'user' in session:
        return redirect(request.referrer)
    else:
        if request.method == "GET":
            if "currentReqPath" not in session:
                session["currentReqPath"] = request.referrer
    if request.method == "POST":
        loginCreds = request.form
        returnPath = session["currentReqPath"]
        userName = str(loginCreds["userName"])
        passW = loginCreds["pWord"]
        passWEncrypted = passEncryption(passW)
        searchQuery = "SELECT userid, passwordhash, adminstatus FROM users WHERE username = '"+userName+"';"
        with conn.cursor() as cur:
            results = []
            loops = 0
            try:
                cur.execute(searchQuery)
                results = cur.fetchall()
                print(results)
            except Exception as ex:
                print(ex)
                conn.rollback()
                return render_template("userRelatedItems/login.html", error="Database error")
        if len(results) != 1:
            return render_template("userRelatedItems/login.html", error="Incorrect Username")
        userHash = (str(Binary(results[0][1])))[1:-8]
        if passWEncrypted == userHash:
            session['user'] = results[0][0]
            if results[0][2] is True:
                session['admin'] = True
            session.pop("currentReqPath")
            conn.close()
            return redirect(returnPath)
        else:
            conn.close()
            return render_template("userRelatedItems/login.html", error="Incorrect Password")
    return render_template("userRelatedItems/login.html")


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("index.home"))
