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

    should_loop = True

    while should_loop:
        bar.update(0)
        if handler.output_queue.empty():
            time.sleep(1 / 30)
        else:
            res = handler.output_queue.get()
            if res:
                args.output.write(print_response(res))
            bar.update(1)

        if handler.hosts_queue.empty() and handler.is_alive() and not handler.has_stopped:
            handler.stop()
        should_loop = handler.is_alive() or not handler.output_queue.empty()

    bar.close()
