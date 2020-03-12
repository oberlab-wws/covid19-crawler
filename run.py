#!/usr/bin/env python

import os
import sys
import argparse
from pathlib import Path
import threading
import csv
#
from covid19_lib.Covid19CrawlerFactory import Covid19CrawlerFactory


def _get_state_crawlers(directory, the_states):
    with open(Path(directory) / 'states.csv', 'r') as states:
        _states_reader = csv.reader(states, dialect = 'excel-tab')
        return [Covid19CrawlerFactory[_state[0]]() for _state in _states_reader if the_states is None or _state[0] in the_states]


def main(DIRECTORY, STATES = None):
    try:
        _input = _get_state_crawlers(DIRECTORY, STATES)
    except Exception as e:
        _input = list()
        print('WARNING: could not generate input data!')
        print(e)
    _output = list()
    #
    nthreads = len(os.sched_getaffinity(0))
    lock = threading.Lock()
    on_input = threading.Condition(lock)
    work_state = {'tasks': len(_input)}

    def _crawl():
        while True:
            with lock:
                while True:
                    if not work_state['tasks']:
                        return
                    if not _input:
                        on_input.wait()
                        continue
                    the_state = _input.pop()
                    break
            try:
                print('BEGUN: {}'.format(the_state.state))
                the_state.crawl()
                with lock:
                    _output.extend([the_state])
                    work_state['tasks'] -= 1
                    on_input.notify()
                print('FINISHED: {}'.format(the_state.state))
            except Exception as e:
                with lock:
                    work_state['tasks'] -= 1
                print(e)
            finally:
                with lock:
                    on_input.notifyAll()

    for w in [threading.Thread(target = _crawl, name = 'crawl %d'.format(i)) for i in range(nthreads)]:
        w.start()

    for output in _output:
        output.write_results()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', dest = 'DIRECTORY', required = True, help = 'looks for states.csv file under this directory for states to crawl, writes results to this directory')
    parser.add_argument('-s', dest = 'STATES', action = 'append', required = False, help = 'filter crawler to scrape information from given states; if not given, crawls states given in states.csv')
    args = parser.parse_args()

    sys.exit(main(**vars(args)))
