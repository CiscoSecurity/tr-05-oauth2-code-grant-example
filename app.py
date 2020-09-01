import os

from flask import Flask

from modules import modules_blueprint
from oauth import oauth_blueprint

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.url_map.strict_slashes = False

app.register_blueprint(modules_blueprint, url_prefix="/modules")
app.register_blueprint(oauth_blueprint)

if __name__ == "__main__":
    app.run()
