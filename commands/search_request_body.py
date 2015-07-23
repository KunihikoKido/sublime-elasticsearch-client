from .base import SearchBaseCommand


class SearchRequestBodyCommand(SearchBaseCommand):
    command_name = "elasticsearch:search-request-body"

    def run_request(self, search_type=None):
        options = dict(
            index=self.settings.index,
            doc_type=self.settings.doc_type,
            body=self.get_text(),
            params={},
            ignore=[404, 400]
        )

        self.extend_options(options, search_type=search_type)

        return self.client.search(**options)
