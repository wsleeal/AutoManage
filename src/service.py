import logging
import socket
import sys
import time

import servicemanager
import win32event
import win32service
import win32serviceutil

logging.basicConfig(filename="service.log", level=logging.ERROR)


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
        while not self.stopped:
            print("All good!", time.time())
            time.sleep(1)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(Service)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(Service)
