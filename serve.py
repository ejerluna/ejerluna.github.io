import subprocess
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class RestartHandler(FileSystemEventHandler):
    def __init__(self):
        self.process = None
        self.start_server()

    def start_server(self):
        if self.process:
            self.process.terminate()
            self.process.wait()

        self.process = subprocess.Popen([
            sys.executable, "-m", "http.server", "8000"
        ])

    def on_any_event(self, event):
        if not event.is_directory:
            self.start_server()

handler = RestartHandler()
observer = Observer()
observer.schedule(handler, ".", recursive=True)
observer.start()

try:
    observer.join()
except KeyboardInterrupt:
    observer.stop()
    if handler.process:
        handler.process.terminate()

observer.join()
