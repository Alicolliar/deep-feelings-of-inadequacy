from flask import Blueprint, render_template
bp = Blueprint('error', __name__)

@bp.route("/tradeError")
def tradeError():
    return render_template("errorPages/tradeError.html")
