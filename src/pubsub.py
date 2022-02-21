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
    def __init__(self, topic: str, broker: "Broker") -> None:
        self.broker = broker
        self.topic = topic

    def notify(self, context):
        self.broker.router(self.topic, context)


class Listener:
    def __init__(self, topic: str, broker: "Broker") -> None:
        broker.add_listener(topic, self)

    def update(self, context):
        print(context)


if __name__ == "__main__":

    __broker = Broker()

    __listener = Listener("Teste", __broker)

    __event = Event("Teste", __broker)
    __event.notify("Oi")
