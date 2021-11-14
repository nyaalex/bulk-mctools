import threading
import queue
from .statusping import StatusPing
import time


class QueryThread(threading.Thread):

    def __init__(self, host_queue, output_queue):
        super().__init__()
        self.kill = threading.Event()
        self.hosts = host_queue
        self.output = output_queue

    def run(self):
        while not self.kill.is_set():
            try:
                # MAIN CODE
                if not self.hosts.empty():
                    host = self.hosts.get()
                else:
                    time.sleep(1/50)
                    continue

                ping = StatusPing(host, 25565, 5)
                status = ping.get_status()
                status['host'] = host

                self.output.put(status)

            except Exception as e:
                print(e)

    def stop(self):
        self.kill.set()


class QueriesHandler:

    def __init__(self, num_threads):
        self.threads = []

        self.output_queue = queue.Queue()
        self.hosts_queue = queue.Queue()

        for i in range(num_threads):
            self.threads.append(QueryThread(self.hosts_queue, self.output_queue))

    def start(self):
        for spammer in self.threads:
            spammer.start()

    def stop(self):
        for spammer in self.threads:
            spammer.stop()
