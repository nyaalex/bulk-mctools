import threading
import queue
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
                    time.sleep(1/20)
                    continue

                ping = StatusPing(host, 25565, self.timeout)
                try:
                    status = ping.get_status()
                    status['host'] = host
                    output = status

                except Exception as e:
                    output = False

                self.output.put_nowait(output)

            except Exception as e:
                raise e

    def stop(self):
        self.kill.set()


class QueriesHandler:

    def __init__(self, num_threads, timeout):
        self._threads = []
        self.has_stopped = False

        self.output_queue = queue.Queue()
        self.hosts_queue = queue.Queue()

        for i in range(num_threads):
            self._threads.append(QueryThread(self.hosts_queue, self.output_queue, timeout))

    def start(self):
        for query_thread in self._threads:
            query_thread.start()

    def is_alive(self):
        x = False
        for query_thread in self._threads:
            x = x or query_thread.is_alive()
        return x

    def stop(self):
        for query_thread in self._threads:
            query_thread.stop()
        self.has_stopped = True
