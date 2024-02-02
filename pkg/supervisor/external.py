import os
import subprocess
import time
from xmlrpc.client import ServerProxy


class SupervisorExternal:

    def __init__(self, url):
        self.__server = ServerProxy(url)

    def run_all_command(self, cmd: str):
        commands = dict(stop_all=self.__stop_all_processes,
                        start_all=self.__start_all_processes,
                        restart_all=self.__restart_all_processes, )
        c = commands.get(cmd)
        if not c:
            return False, "Command not found"
        res, err = c()
        return res, err

    def __restart_all_processes(self):
        try:
            self.__server.supervisor.stopAllProcesses()
            self.__server.supervisor.startAllProcesses()
            return True, None
        except Exception as e:
            return False, e.__str__()

    def __stop_all_processes(self):
        try:
            self.__server.supervisor.stopAllProcesses()
            return True, None
        except Exception as e:
            return False, e.__str__()

    def __start_all_processes(self):
        try:
            self.__server.supervisor.startAllProcesses()
            return True, None
        except Exception as e:
            return False, e.__str__()

    def stop_process(self, name: str):
        try:
            self.__server.supervisor.stopProcess(name)
            return True, None
        except Exception as e:
            return False, e.__str__()

    def start_process(self, name: str):
        try:
            self.__server.supervisor.startProcess(name)
            return True, None
        except Exception as e:
            return False, e.__str__()

    def restart_process(self, name: str):
        try:
            self.__server.supervisor.stopProcess(name)
            self.__server.supervisor.startProcess(name)
            return True, None
        except Exception as e:
            return False, e.__str__()
