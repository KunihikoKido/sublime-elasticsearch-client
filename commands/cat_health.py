from .base import CatBaseCommand


class CatHealthCommand(CatBaseCommand):

    def run_request(self):
        options = dict(
            params=dict(v=1)
        )

        return self.client.cat.health(**options)
