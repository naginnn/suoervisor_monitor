from pkg.supervisor.external import SupervisorExternal
from pkg.supervisor.internal import SupervisorInternal
from pkg.supervisor.signals import SupervisorInfo


class SupervisorClient:

    def __init__(self, url):
        self.info = SupervisorInfo(url=url)
        self.internal = SupervisorInternal(url=url)
        self.external = SupervisorExternal(url=url)


if __name__ == '__main__':
    supervisor = SupervisorClient(url='http://user:123@localhost:9001/RPC2')
    print(supervisor.info.get_processes_info())
