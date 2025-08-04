from ansys.meshing.prime import launch_prime
from Mesh.misc.PATHS import ANSYS_PRIME
from ansys.meshing.prime.internals.client import Client


class PrimeClient:
    """
    Class for describe a prime client.
    """
    def __init__(self):
        self._client = self.__launch()

        # print client status
        print(self._client)

    @property
    def client(self) -> Client:
        """
        Get prime client.

        Return:
            Client: prime client
        """
        return self._client

    @staticmethod
    def __launch() -> Client:
        """
        Launch prime client.

        Return:
            Client: prime client
        """
        return launch_prime(
            prime_root=ANSYS_PRIME,
            timeout=120
        )

    def exit(self):
        """
        Exit prime client.

        """
        self._client.exit()
