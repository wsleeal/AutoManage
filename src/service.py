import logging
import socket
import sys
import time

import psutil
import servicemanager
import win32event
import win32service
import win32serviceutil

import main
import pubsub


class Service(win32serviceutil.ServiceFramework):
    _svc_name_ = "AutoRestartServer"
    _svc_display_name_ = "Auto Restart Server"
    _svc_description_ = "Auto Restart Server"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcDoRun(self):
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE, servicemanager.PYS_SERVICE_STARTED, (self._svc_name_, "")
        )
        self.main()

    def SvcStop(self):
        self.stopped = True
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def main(self):
        self.stopped = False
        broker = pubsub.Broker()
        main.MemoriaListener(broker)
        eventos = main.Events(broker)
        while not self.stopped:
            eventos.memoria_porcent = psutil.virtual_memory()
            eventos.check_restart()
            time.sleep(1)


if __name__ == "__main__":
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    fh = logging.FileHandler("console.log")
    fh.setLevel(logging.ERROR)
    formatter = "[%(asctime)s file:%(name)s line:%(lineno)s]%(levelname)s: %(message)s"
    datefmt = "%m/%d/%Y %H:%M:%S"
    logging.basicConfig(handlers=(ch, fh), datefmt=datefmt, format=formatter, level=logging.INFO)

    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(Service)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(Service)
