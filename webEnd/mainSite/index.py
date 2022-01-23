from flask import Blueprint, render_template

bp = Blueprint('index', __name__)
@bp.route('/')
def home():
    return render_template("home.html")


@bp.route('/faqs')
def catchMost():
    return render_template("faqPage.html")


@bp.route('/compliance')
def compliance():
    return render_template("compliance.html")
