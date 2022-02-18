import os
import sys
import time
import json
import webview
from flask import Flask, render_template, jsonify, request
from functools import wraps
import getpass  # get user

# Template directory
if sys.flags.dev_mode:
    MAIN_DIR = os.path.join("..", "dist")  # development
else:
    MAIN_DIR = os.path.join(".", "dist")  # production

FIRST_LAUNCH = True

server = Flask(__name__, template_folder=MAIN_DIR, static_folder=MAIN_DIR, static_url_path="/")
server.config["SEND_FILE_MAX_AGE_DEFAULT"] = 1


def verify_token(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        data = json.loads(request.data)
        token = data.get("token")
        if token == webview.token:
            return function(*args, **kwargs)
        else:
            raise Exception("Authentication error")

    return wrapper


@server.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store"
    return response


@server.route("/", defaults={"path": ""})
@server.route("/<path:path>")
def serve(path):
    # Handle first launch on development stage
    global FIRST_LAUNCH

    if FIRST_LAUNCH and sys.flags.dev_mode:
        time.sleep(2.5)
        FIRST_LAUNCH = False

    return render_template("index.html", token=webview.token)


@server.route("/init", methods=["POST"])
@verify_token
def initialize():
    return jsonify({"user": getpass.getuser()})
