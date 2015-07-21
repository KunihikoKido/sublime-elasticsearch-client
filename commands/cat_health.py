from .base import CatBaseCommand


class CatHealthCommand(CatBaseCommand):
    command_name = "elasticsearch:cat-health"

    def run_request(self):
        options = dict(
            params=dict(v=1)
        )

        return self.client.cat.health(**options)
