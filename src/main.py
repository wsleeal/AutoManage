import logging
import os

import psutil

import pubsub


class MemoriaManager(pubsub.Listener):
    def __init__(self, broker: "pubsub.Broker") -> None:
        super().__init__("memoria_view", broker)
        self.memoria_log = list()

    def update(self, context):
        try:
            self.memoria_log.append(int(context))
            if len(self.memoria_log) > 900:
                if (sum(self.memoria_log) / len(self.memoria_log)) > 85:
                    os.system("shutdown -r -f -t 1")
                else:
                    self.memoria_log.clear()
        except:
            raise logging.exception("")


class MemoriaView(pubsub.Event):
    _em_uso = None

    def __init__(self, broker: "pubsub.Broker") -> None:
        super().__init__("memoria_view", broker)

    @property
    def em_uso(self):
        return self._em_uso

    @em_uso.setter
    def em_uso(self, valor):
        self._em_uso = valor
        self.notify(valor)


if __name__ == "__main__":
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    fh = logging.FileHandler("console.log")
    fh.setLevel(logging.ERROR)
    formatter = "%(asctime)s %(levelname)s: %(message)s"
    datefmt = "%m/%d/%Y %H:%M:%S"
    logging.basicConfig(handlers=(ch, fh), datefmt=datefmt, format=formatter, level=logging.DEBUG)

    broker = pubsub.Broker()
    memoria_manager = MemoriaManager(broker)
    memoria_view = MemoriaView(broker)
    memoria_view.em_uso = psutil.virtual_memory().percent
