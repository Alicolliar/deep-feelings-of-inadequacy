from flask import Flask
import importlib
app = Flask(__name__)


def create_app():
    app = Flask(__name__)
    baseModules = (
        "public",
        "private"
    )
    for modname in baseModules:
        mod = importlib.import_module("apiSite." + modname)
        bp = mod.bp
        app.register_blueprint(bp, url_prefix="/" + modname)
    return app
