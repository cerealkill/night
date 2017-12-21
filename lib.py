import pickle
import sys
import time
import threading
from pathlib import Path

import os
import colorlog

handler = colorlog.StreamHandler()
# %(log_color)s%(asctime)s - %(levelname)s - %(message)s
handler.setFormatter(colorlog.ColoredFormatter('%(log_color)s%(message)s'))

# Default color scheme is 'example'
logger = colorlog.getLogger('example')
logger.addHandler(handler)


def save(file_name, data):
    with open(file_name, 'w+') as file:
        file.write(data)


class Memory:

    def __init__(self, file):
        home_path = str(Path.home().joinpath('.night/'))
        if not os.path.exists(home_path):
            os.makedirs(home_path)
        self.file = home_path + file
        self.memory = pickle.load(open(self.file, 'rb'))

    def save_memory(self, memory):
        pickle.dump(memory, open(self.file, 'wb'), protocol=pickle.HIGHEST_PROTOCOL)


class Spinner:
    busy = False
    delay = 0.1

    @staticmethod
    def spinning_cursor():
        while 1:
            for cursor in '|/-\\': yield cursor

    def __init__(self, delay=None):
        self.spinner_generator = self.spinning_cursor()
        if delay and float(delay): self.delay = delay

    def spinner_task(self):
        while self.busy:
            sys.stdout.write(next(self.spinner_generator))
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write('\b')
            sys.stdout.flush()

    def start(self):
        self.busy = True
        threading.Thread(target=self.spinner_task).start()

    def stop(self):
        self.busy = False
        time.sleep(self.delay)


class AsyncClientError(EnvironmentError):
    pass
