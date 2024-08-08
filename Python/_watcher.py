import os
import sys
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

class MyHandler(PatternMatchingEventHandler):
    def __init__(self, patterns):
        super().__init__(patterns=patterns)
        self.processes = {}
        for pattern in patterns:
            self.start_process(pattern)

    def start_process(self, script_name):
        process = subprocess.Popen([sys.executable, script_name])
        self.processes[script_name] = process

    def on_modified(self, event):
        script_name = event.src_path
        if script_name in self.processes:
            self.processes[script_name].terminate()
            self.processes[script_name].wait()
            self.start_process(script_name)

if __name__ == "__main__":
    scripts_to_watch = ['RecTest.py']
    event_handler = MyHandler(scripts_to_watch)
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
