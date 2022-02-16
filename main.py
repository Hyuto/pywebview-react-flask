import os
from server import server
import webview

DEBUG = True


def WebViewApp():
    server.debug = DEBUG
    window = webview.create_window("react-flask-pywebview-app", server)
    webview.start(debug=DEBUG)


if __name__ == "__main__":
    WebViewApp()
