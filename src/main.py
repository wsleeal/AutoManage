import json
import logging
import os
from pathlib import Path

import psutil

import pubsub


def get_config():
    configs = Path(Path(__file__).parent, "configs.json")
    if configs.exists():
        with open(configs, "r") as f:
            return json.loads(f.read())
    else:
        with open(configs, "w") as f:
            dados = dict()
            dados["debug"] = True
            dados["restart_now"] = False
            dados["time_test"] = 36000
            dados["percent_test"] = 100
            json.dump(dados, f, indent=4)
            return dados


class MemoriaListener(pubsub.Listener):
    def __init__(self, broker: "pubsub.Broker") -> None:
        super().__init__("memoria_porcet", broker)
        self.memoria_log = list()

    def update(self, context):
        config = get_config()
        if not isinstance(context, psutil._pswindows.svmem):
            return logging.error("MemoriaManager: Contexto Invalido")

        self.memoria_log.append(context.percent)
        log_length = len(self.memoria_log)
        logging.debug(f"MemoriaManager: {log_length}/{config['time_test']}")
        if log_length > config["time_test"]:
            if (sum(self.memoria_log) / log_length) > config["percent_test"]:
                if not config["debug"]:
                    os.system("shutdown -r -f -t 1")
                else:
                    logging.debug("MemoriaManager: Reiniciou")
            self.memoria_log.clear()


class Events(pubsub.Event):
    _memoria_porcent = None

    def __init__(self, broker: "pubsub.Broker") -> None:
        super().__init__(broker)

    @property
    def memoria_porcent(self):
        return self._memoria_porcent

    @memoria_porcent.setter
    def memoria_porcent(self, valor):
        self._memoria_porcent = valor
        self.notify("memoria_porcet", valor)

    def check_restart(self):
        config = get_config()
        if config["restart_now"] == True:
            with open("configs.json", "r+") as f:
                config["restart_now"] = False
                json.dump(config, f, indent=4)
                if not config["debug"]:
                    os.system("shutdown -r -f -t 1")
                else:
                    logging.debug("check_restart: Restarted")


if __name__ == "__main__":
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    fh = logging.FileHandler("console.log")
    fh.setLevel(logging.ERROR)
    formatter = "[%(asctime)s file:%(name)s line:%(lineno)s]%(levelname)s: %(message)s"
    datefmt = "%m/%d/%Y %H:%M:%S"
    logging.basicConfig(handlers=(ch, fh), datefmt=datefmt, format=formatter, level=logging.INFO)

    broker = pubsub.Broker()
    memoria_manager = MemoriaListener(broker)
    eventos = Events(broker)

    eventos.memoria_porcent = psutil.virtual_memory()
    eventos.check_restart()
