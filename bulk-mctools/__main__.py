import argparse
import fileinput
import time
from .query_thread import QueriesHandler

parser = argparse.ArgumentParser()


handler = QueriesHandler(50)
handler.start()

for line in fileinput.input():
    handler.hosts_queue.put(line.strip())

while not handler.hosts_queue.empty():
    if handler.output_queue.empty():
        time.sleep(1)
    else:
        print(handler.output_queue.get())

handler.stop()

while not handler.output_queue.empty():
    print(handler.output_queue.get())
