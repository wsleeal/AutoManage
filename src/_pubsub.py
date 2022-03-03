class Broker:
    def __init__(self) -> None:
        self.listeners: dict[str, set[Listener]] = dict()

    def add_listener(self, topic: str, listener: "Listener"):
        if topic in self.listeners:
            self.listeners[topic].add(listener)
        else:
            self.listeners[topic] = {listener}

    def router(self, topic: str, context):
        if topic in self.listeners:
            for listener in self.listeners[topic]:
                listener.update(context)


class Event:
    def __init__(self, broker: "Broker") -> None:
        self.broker = broker

    def notify(self, topic: str, context):
        self.broker.router(topic, context)


class Listener:
    def __init__(self, broker: "Broker") -> None:
        self.broker = broker

    def onEvent(self, topic: str, callback):
        self.broker.add_listener(topic, self)
        self.update = callback

    def update(self, context):
        raise NotImplementedError


if __name__ == "__main__":

    def callback(context):
        print("Contexto recebido: ", context)

    broker = Broker()

    listener = Listener(broker)
    listener.addListener("Teste", callback)

    event = Event(broker)
    event.notify("Teste", "Oi")
