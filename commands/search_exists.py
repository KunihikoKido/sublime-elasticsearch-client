from .base import BaseCommand


class SearchExistsCommand(BaseCommand):
    command_name = "elasticsearch:search-exists"

    def run_request(self):
        options = dict(
            index=self.settings.index,
            doc_type=self.settings.doc_type,
            body=self.get_text(),
            ignore=[404]
        )

        return self.client.search_exists(**options)
