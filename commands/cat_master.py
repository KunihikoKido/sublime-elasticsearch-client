from .base import CatBaseCommand


class CatMasterCommand(CatBaseCommand):

    def run_request(self):
        options = dict(
            params=dict(v=1)
        )

        return self.client.cat.master(**options)
