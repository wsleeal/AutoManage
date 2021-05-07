from abc import ABC, abstractmethod
from typing import Type, List


class PubSub(ABC):

    @abstractmethod
    def __init__(self):
        self._subscribers: List["Subscriber"] = []

    @abstractmethod
    def attach(self, subscriber: Type["Subscriber"]):
        if subscriber not in self._subscribers:
            self._subscribers.append(subscriber)

    @abstractmethod
    def detach(self, subscriber: Type["Subscriber"]):
        if subscriber in self._subscribers:
            self._subscribers.remove(subscriber)

    @abstractmethod
    def route(self, msg, topic):
        for subscriber in self._subscribers:
            if topic in subscriber.topic:
                subscriber.sub(msg, topic)

class Subscriber(ABC):

    @abstractmethod
    def __init__(self, name, pubsub: Type["PubSub"], topic: list):
        self._name = name
        if not isinstance(topic, list):
            raise ValueError(f"Erro: {topic} nao e uma lista")
        self.topic = topic
        pubsub.attach(self)
    
    @abstractmethod
    def sub(self, msg, topic):
        print(self._name, msg, self.topic)


class Publisher(ABC):

    @abstractmethod
    def __init__(self, pubsub: Type["PubSub"]):
        self._pubsub = pubsub

    @abstractmethod
    def pub(self, msg, topic):
        self._pubsub.route(msg, topic)



if __name__ == "__main__":

    class Proxy(PubSub):
        def __init__(self):
            super().__init__()

        def attach(self, subscriber):
            super().attach(subscriber)

        def detach(self, subscriber):
            super().detach(subscriber)

        def route(self, msg, topic):
            super().route(msg, topic)

    class Server(Publisher):
        def __init__(self, pubsub):
            super().__init__(pubsub)

        def pub(self, msg, topic):
            super().pub(msg, topic)
    
    class Client(Subscriber):
        def __init__(self, name, pubsub, topic):
            super().__init__(name, pubsub, topic)
        
        def sub(self, msg, topic):
            super().sub(msg, topic)


    proxy = Proxy()

    server = Server(proxy)

    client = Client("William", proxy, ["A"])

    server.pub("Oi", "A")