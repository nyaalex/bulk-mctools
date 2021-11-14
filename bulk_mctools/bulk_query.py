import argparse
import fileinput
import time
from .query_thread import QueriesHandler
from .printer import print_response


def run():
    parser = argparse.ArgumentParser(description='Query Minecraft servers in bulk')

    parser.add_argument('--threads', '-t', default=10, type=int, help='Number of threads')
    parser.add_argument('input', type=argparse.FileType('r'), help='IP address file')

    args = parser.parse_args()

    handler = QueriesHandler(args.threads)
    handler.start()

    for line in args.input:
        handler.hosts_queue.put(line.strip())

    while not handler.hosts_queue.empty():
        if handler.output_queue.empty():
            time.sleep(1)
        else:
            print(print_response(handler.output_queue.get()))

    handler.stop()

    while not handler.output_queue.empty():
        print(print_response(handler.output_queue.get()))


if __name__ == '__main__':
    run()
