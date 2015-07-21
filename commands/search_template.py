from .base import SearchBaseCommand


class SearchTemplateCommand(SearchBaseCommand):
    command_name = "elasticsearch:search-template"

    def run_request(self, search_type=None):
        options = dict(
            index=self.settings.index,
            doc_type=self.settings.doc_type,
            body=self.get_text(),
            params={},
            ignore=[404, 400]
        )

        self.extend_options(options, search_type=search_type)

        return self.client.search_template(**options)
