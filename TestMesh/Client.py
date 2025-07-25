import ansys.meshing.prime as prime
from misc.PATHS import ANSYS_Prime


class Client:
    def __init__(self):
        self._client = self.__launch()
        print(self._client)

    @property
    def client(self):
        return self._client

    def __launch(self):
        print('Launching....')
        #return prime.Client(ip="127.0.0.1", port=50055)
        return prime.launch_prime(
            prime_root=ANSYS_Prime,
            ip="79.188.195.106",
            port=1055,
            n_procs=2,
            timeout=120
        )

    def exit(self):
        self._client.exit()


if __name__ == '__main__':
    client = Client()
    client.exit()
