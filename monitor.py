"""
Yield each changed source file, as a pathlib.Path

Runs indefinitely. Exit with Ctrl-C
"""

import collections
import queue
import watchdog.observers
import watchdog.events
import time

class FunctionEventHandler(watchdog.events.FileSystemEventHandler):
    def __init__(self, f):
        self.f = f
    def on_any_event(self, event):
        self.f(event)

class Monitor():
    def __init__(self, path, discard_rapid=None):
        self.observer = watchdog.observers.Observer()
        self.updates = queue.Queue()
        self.observer.schedule(
            FunctionEventHandler(self.updates.put),
            path,
            recursive=True
        )
        self.last_update = collections.defaultdict(int)
        self.discard_rapid = discard_rapid
        self.observer.start()

    @staticmethod
    def time():
        return time.time()

    def is_rapid(self, path):
        now = self.time()
        last = self.last_update[path]
        elapsed = now - last
        return (self.discard_rapid is not None and 
                elapsed < self.discard_rapid)

    ignore_events = [
        watchdog.events.FileOpenedEvent,
        watchdog.events.FileClosedEvent,
        watchdog.events.DirModifiedEvent,
    ]
    def _iter(self):
        try:
            while True:
                event = self.updates.get()
                if not any(isinstance(event, t) for t in self.ignore_events):
                    yield event.src_path
                    if hasattr(event, "dest_path"):
                        yield event.dest_path
                self.updates.task_done()
        except KeyboardInterrupt:
            self.observer.stop()
            self.observer.join()

    def __iter__(self):
        for x in self._iter():
            if not self.is_rapid(x):
                yield x
