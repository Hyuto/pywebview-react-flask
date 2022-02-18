import os
import sys
from server import server
import webview

DEBUG = True


def WebViewApp():
    server.debug = DEBUG
    window = webview.create_window("react-flask-pywebview-app", server)
    webview.start(debug=DEBUG)


if __name__ == "__main__":
    if sys.flags.dev_mode:
        # Please don't delete code bellow to enable
        # auto reload when your react code have changes
        from utils import run_frontend_watcher

        template_dir = os.path.join(os.getcwd(), "src", "frontend")
        run_frontend_watcher(template_dir=template_dir)

    WebViewApp()
