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
        if not event.is_directory:
            _, src_path = os.path.split(event.src_path)
            print(f"Detected changes in {src_path}, refreshing ...")
            for window in webview.windows:
                window.evaluate_js(r"window.location.reload()")


class Watcher:
    def __init__(self, template_dir):
        self.observer = Observer()
        self.directory_to_watch = template_dir

    def _wait_first_launch(self):
        while not os.path.exists(self.directory_to_watch):
            time.sleep(0.5)

    def run(self):
        self._wait_first_launch()

        event_handler = Handler()
        self.observer.schedule(event_handler, self.directory_to_watch, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        finally:
            self.observer.stop()
            self.observer.join()


def run_frontend_watcher(template_dir):
    watcher = Watcher(template_dir)

    background_thread = threading.Thread(target=watcher.run, args=())
    background_thread.daemon = True
    background_thread.start()
