import sys
import argparse
import time
from .query_thread import QueriesHandler
from .printer import print_response
from tqdm import tqdm


def run():
    parser = argparse.ArgumentParser(description='Query Minecraft servers in bulk')

    parser.add_argument('--threads', '-t', default=10, type=int, help='Number of threads')
    parser.add_argument('--timeout', '-T', default=5, type=int, help='Server timeout')
    parser.add_argument('--output', '-o', default='-', type=argparse.FileType('w'), help='output file')
    parser.add_argument('--input', '-i', default='-', type=argparse.FileType('r'), help='input file')

    args = parser.parse_args()

    handler = QueriesHandler(args.threads, args.timeout)
    handler.start()

    host_count = 0

    for line in args.input:
        handler.hosts_queue.put(line.strip())
        host_count += 1

    bar = tqdm(total=host_count)

    while not handler.hosts_queue.empty():
        if handler.output_queue.empty():
            time.sleep(1/20)
        else:
            res = handler.output_queue.get()
            if res:
                args.output.write(print_response(res))
            bar.update(1)

    bar.close()
    handler.stop()

    while not handler.output_queue.empty():
        res = handler.output_queue.get()
        if res:
            args.output.write(print_response(res))
        bar.update(1)
    bar.close()


if __name__ == '__main__':
    run()
