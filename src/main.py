import json
import logging
import os
from pathlib import Path

import psutil

import pubsub


def get_config():
    config = Path(Path(__file__).parent.parent, "config.json")
    if config.exists():
        with open(config, "r") as f:
            return json.loads(f.read())
    else:
        with open(config, "w") as f:
            dados = dict()
            dados["debug"] = True
            dados["restart_now"] = False
            dados["time_test"] = 36000
            dados["percent_test"] = 100
            dados["config_path"] = str(config)
            json.dump(dados, f, indent=4)
            logging.info("Config.json Criado")
            return dados


class MemoriaListener(pubsub.Listener):
    def __init__(self, broker: "pubsub.Broker") -> None:
        super().__init__("memoria_status", broker)
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
    _memoria_status = None

    def __init__(self, broker: "pubsub.Broker") -> None:
        super().__init__(broker)

    @property
    def memoria_status(self):
        return self._memoria_status

    @memoria_status.setter
    def memoria_status(self, valor):
        self._memoria_status = valor
        self.notify("memoria_status", valor)

    def check_restart(self):
        config = get_config()
        if config["restart_now"] == True:
            with open(config["config_path"], "r+") as f:
                config["restart_now"] = False
                json.dump(config, f, indent=4)
                if not config["debug"]:
                    os.system("shutdown -r -f -t 1")
                else:
                    logging.debug("check_restart: Restarted")


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)

    broker = pubsub.Broker()
    MemoriaListener(broker)

    eventos = Events(broker)

    eventos.memoria_status = psutil.virtual_memory()
    eventos.check_restart()
