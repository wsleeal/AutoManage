from src._pubsub import Broker, Event, Listener


class Teste:
    def __init__(self) -> None:
        self.msg = "Testando ..."

    def callback(self, context):
        print(self.msg, context)


t = Teste()


b = Broker()
l = Listener(b)
l.onEvent("Teste", t.callback)
e = Event(b)
e.notify("Teste", "Oi")
