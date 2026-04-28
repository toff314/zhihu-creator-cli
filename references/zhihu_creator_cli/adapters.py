"""Force IPv4 for all HTTP requests.

Works around IPv6 connectivity issues by binding to 0.0.0.0 (IPv4 only).
"""

import socket

from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager


class ForceIPv4Adapter(HTTPAdapter):
    """HTTPAdapter that forces IPv4 connections.

    Mount this on a requests.Session to avoid IPv6 timeouts:

        session = requests.Session()
        session.mount("https://", ForceIPv4Adapter())
        session.mount("http://", ForceIPv4Adapter())
    """

    def init_poolmanager(self, connections, maxsize, block=False, **pool_kwargs):
        # source_address=0.0.0.0 forces urllib3 to pick IPv4 family
        self.poolmanager = PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            source_address=("0.0.0.0", 0),
            **pool_kwargs,
        )
