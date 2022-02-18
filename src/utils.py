"""
Script to apply auto reload in development while running "yarn start"
if any changes detected on react code (in 'src' directory)
"""

import os
import time
import threading
import webview
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        print(f"Detected changes in template, refreshing ...")
        for window in webview.windows:
            window.evaluate_js(r"window.location.reload()")


class Watcher:
    def __init__(self, template_dir):
        self.observer = Observer()
        self.DIRECTORY_TO_WATCH = template_dir

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        finally:
            self.observer.stop()
            self.observer.join()


def run_frontend_watcher(template_dir):
    w = Watcher(template_dir)

    background_thread = threading.Thread(target=w.run, args=())
    background_thread.daemon = True
    background_thread.start()
