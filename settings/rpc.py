from xmlrpc.client import ServerProxy

from pkg.supervisor.client import SupervisorClient


async def get_rpc_client():
    return SupervisorClient(url='http://user:123@localhost:9001/RPC2')