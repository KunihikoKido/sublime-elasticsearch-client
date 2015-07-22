from .base import BaseCommand


class SearchShardsCommand(BaseCommand):
    command_name = "elasticsearch:search-shards"

    def is_enabled(self):
        return True

    def run_request(self):
        options = dict(
            index=self.settings.index
        )

        return self.client.search_shards(**options)
