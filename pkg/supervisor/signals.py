import os
import subprocess
import time
from typing import Union
from xmlrpc.client import ServerProxy


class SupervisorInfo:

    def __init__(self, url):
        self.__server = ServerProxy(url)

    def get_all_config(self):
        try:
            config = self.__server.supervisor.getAllConfigInfo()
            names = [c.get("name") for c in config]
            pid = self.__server.supervisor.getPID()
            return dict(config=config, names=names, pid=pid), None
        except Exception as e:
            return None, e.__str__()

    def get_processes_info(self):
        try:
            apps = self.__server.supervisor.getAllProcessInfo()
            state = self.__server.supervisor.getState().get("statename").lower()
            return dict(apps=apps, state=state), None
        except Exception as e:
            return None, e.__str__()

    def get_process_info(self, name: str):
        try:
            proc = self.__server.supervisor.getProcessInfo(name)
            return proc, None
        except Exception as e:
            return None, e.__str__()

    def tail_process_stdout_log(self, name: str):
        try:
            log = self.__server.supervisor.tailProcessStdoutLog(name, 0, 2000000)
            return log[0], None
        except Exception as e:
            return None, e.__str__()

    def tail_process_stderr_log(self, name: str):
        try:
            log = self.__server.supervisor.tailProcessStderrLog(name, 0, 2000000)
            return log[0], None
        except Exception as e:
            return None, e.__str__()
