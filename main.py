import logging
import os
import socket
import sys

import psutil
import servicemanager
import win32event
import win32service
import win32serviceutil

logging.basicConfig(filename="service.log", level=logging.ERROR)


def reiniciar_por_uso_de_recurso(recurso_log: list, percent: int):
    media = sum(recurso_log) / len(recurso_log)
    if media > percent:
        os.system("shutdown -r -f -t 1")
        recurso_log.clear()


class Service(win32serviceutil.ServiceFramework):
    _svc_name_ = "AutoManagerServerService"
    _svc_display_name_ = "Auto Manager Server Service"
    _svc_description_ = "Auto Manager Server Service"

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
        memoria_log = list()
        processador_log = list()
        while not self.stopped:
            memoria_log.append(psutil.virtual_memory()._asdict()["percent"])
            processador_log.append(psutil.cpu_percent(interval=1))

            if len(memoria_log) > 10:
                reiniciar_por_uso_de_recurso(memoria_log, 80)
                reiniciar_por_uso_de_recurso(processador_log, 80)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(Service)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(Service)
