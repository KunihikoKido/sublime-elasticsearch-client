from .base import CatBaseCommand


class CatFielddataCommand(CatBaseCommand):
    command_name = "elasticsearch:cat-fielddata"

    def run_request(self):
        options = dict(
            params=dict(v=1)
        )

        return self.client.cat.fielddata(**options)
