from flask import Flask
import importlib
app = Flask(__name__)


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="FMQjoaBUDs",
        HEADER_NAME="Helium Exchange",
        STORED_DATA_PATH="finLogs/"
    )
    baseModules = (
        "index",
        "view",
        "userRelated",
        "trading",
        "superUser",
        "apiRoutes"
    )
    for modname in baseModules:
        mod = importlib.import_module("mainSite." + modname)
        bp = mod.bp
        app.register_blueprint(bp, url_prefix="/" + modname)
    app.add_url_rule("/", endpoint="index.home")

    return app
