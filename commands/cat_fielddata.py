from .base import CatBaseCommand


class CatFielddataCommand(CatBaseCommand):

    def run_request(self):
        options = dict(
            params=dict(v=1)
        )

        return self.client.cat.fielddata(**options)
