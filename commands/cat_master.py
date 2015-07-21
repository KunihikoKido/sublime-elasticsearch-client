from .base import CatBaseCommand


class CatMasterCommand(CatBaseCommand):
    command_name = "elasticsearch:cat-master"

    def run_request(self):
        options = dict(
            params=dict(v=1)
        )

        return self.client.cat.master(**options)
