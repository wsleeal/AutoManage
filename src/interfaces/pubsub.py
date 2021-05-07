from abc import ABC, abstractmethod
from typing import Type, List


class PubSub(ABC):
    """
    Classe faz o registro do inscritos e notifica os inscritos que estao intresados no topic do metodo route

    Usage:

        proxy = PubSub()
    
    """

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
            if topic in subscriber.topics:
                subscriber.sub(msg, topic)

class Subscriber(ABC):
    """
    Clase de inscrito, é instanciada passando o parametro da Classe PubSub
    Sempre que um Publisher fizer uma publicar o PubSub notificara o Inscrito que tiver interece no topico

    Usage:

        proxy = PubSub()

        william = Subscriber("William", proxy, ["CARROS", "MODA"])

    """

    @abstractmethod
    def __init__(self, name, pubsub: Type["PubSub"], topics: list):
        self._name = name
        if not isinstance(topics, list):
            raise ValueError(f"Erro: {topics} nao e uma lista")
        self._topics = topics
        pubsub.attach(self)
    
    @abstractmethod
    def sub(self, msg, topic):
        print(self._name, msg, self._topics)

    @property
    def topics(self):
        return self._topics


class Publisher(ABC):
    """
    Classe responsavel por publicar eventos, quando um evento é publicado o metodo pub notifica a Class
    PubSub e a classe envia a msg para os inscritos interesados no topicos do metodo pub

    Usage:

        proxy = PubSub()

        william = Subscriber("William", proxy, ["CARROS", "MODA"])

        blog = Publisher(proxy)

        blog.pub("Fashion Week Dia 15",["MODA"])

    """

    @abstractmethod
    def __init__(self, pubsub: Type["PubSub"]):
        self._pubsub = pubsub

    @abstractmethod
    def pub(self, msg: str, topics: list):
        if not isinstance(topics, list):
            raise ValueError(f"Erro: {topics} nao e uma lista")
        for topic in topics:
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

        def pub(self, msg, topics: list):
                super().pub(msg, topics)
    
    class Client(Subscriber):
        def __init__(self, name, pubsub, topic):
            super().__init__(name, pubsub, topic)
        
        def sub(self, msg, topics):
            super().sub(msg, topics)


    proxy = Proxy()

    server = Server(proxy)

    client = Client("William", proxy, ["A"])
    client2 = Client("Irmao", proxy, ["B"])

    server.pub("Oi", ["A", "B"])