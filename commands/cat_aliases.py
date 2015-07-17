from .base import CatBaseCommand


class CatAliasesCommand(CatBaseCommand):

    def is_enabled(self):
        return True

    def run_request(self):
        options = dict(
            params=dict(v=1)
        )

        return self.client.cat.aliases(**options)
