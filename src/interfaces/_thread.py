from threading import Thread, Lock
import time

class Processo:

    stopped = True
    numeros = []

    def __init__(self):
        self.lock = Lock()

    def start(self):
        self.stopped = False
        t = Thread(target=self.main)
        t.start()

    def stop(self):
        self.stopped = True

    def main(self):
        while not self.stopped:

            self.lock.acquire()
            self.numeros.append(numero)
            self.lock.release()
        
