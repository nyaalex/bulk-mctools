import threading
import queue
import sys
from .statusping import StatusPing
import time


class QueryThread(threading.Thread):

    def __init__(self, host_queue, output_queue, timeout):
        super().__init__()
        self.kill = threading.Event()
        self.hosts = host_queue
        self.output = output_queue
        self.timeout = timeout

    def run(self):
        while not self.kill.is_set():
            try:
                # MAIN CODE
                if not self.hosts.empty():
                    host = self.hosts.get_nowait()
                else:
                    time.sleep(1/50)
                    continue

                ping = StatusPing(host, 25565, self.timeout)
                try:
                    status = ping.get_status()
                    status['host'] = host
                    self.output.put(status)

                except Exception as e:
                    self.output.put(False)

            except Exception as e:
                print(e, file=sys.stderr)

    def stop(self):
        self.kill.set()


class QueriesHandler:

    def __init__(self, num_threads, timeout):
        self.threads = []

        self.output_queue = queue.Queue()
        self.hosts_queue = queue.Queue()

        for i in range(num_threads):
            self.threads.append(QueryThread(self.hosts_queue, self.output_queue, timeout))

    def start(self):
        for query_thread in self.threads:
            query_thread.start()

    def stop(self):
        for query_thread in self.threads:
            query_thread.stop()
