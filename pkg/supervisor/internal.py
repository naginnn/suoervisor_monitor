import os
import subprocess
import time
from xmlrpc.client import ServerProxy


class SupervisorInternal:

    def __init__(self, url):
        self.__server = ServerProxy(url)

    def run_command(self, cmd: str):
        commands = dict(shutdown=self.__shutdown,
                        restart=self.__restart,
                        clear_log=self.__clear_log,
                        reload_config=self.__reload_config,
                        shutdown_and_apply_config=self.__shutdown_and_apply_config,
                        kill_all_python_processes=self.__kill_all_python_processes)
        c = commands.get(cmd)
        if not c:
            return False, "Command not found"
        res, err = c()
        return res, err

    def __shutdown(self):
        try:
            res = self.__server.supervisor.shutdown()
            return res, None
        except Exception as e:
            return False, e.__str__()

    def __restart(self):
        try:
            res = self.__server.supervisor.restart()
            return res, None
        except Exception as e:
            return False, e.__str__()

    def __clear_log(self):
        try:
            res = self.__server.supervisor.clearLog()
            return res, None
        except Exception as e:
            return False, e.__str__()

    def __reload_config(self):
        try:
            res = self.__server.supervisor.reloadConfig()
            return res, None
        except Exception as e:
            return False, e.__str__()

    def __shutdown_and_apply_config(self):
        try:
            self.__server.supervisor.shutdown()
        except Exception as e:
            pass
        supervisor_conf_path = os.environ.get("SUPERVISOR_CONF_PATH")
        supervisor_conf_path = "/Users/sergeyesenin/PycharmProjects/pythonProject6/supervisord.conf"
        subprocess.Popen(['supervisord', '-c', supervisor_conf_path])
        retrying = 30
        while True:
            try:
                pid = self.__server.supervisor.getPID()
                if pid:
                    return True, None
            except Exception as e:
                time.sleep(1)
                retrying -= 1
                if retrying <= 0:
                    return False, e.__str__()

    # deprecated
    def __kill_all_python_processes(self):
        os.system("ps aux | grep python | grep -v \"grep python\" | awk '{print $2}' | xargs kill -9")


