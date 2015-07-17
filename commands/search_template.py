from .base import SearchBaseCommand


class SearchTemplateCommand(SearchBaseCommand):

    def run_request(self, search_type=None):
        options = dict(
            index=self.settings.index,
            doc_type=self.settings.doc_type,
            body=self.get_text(),
            params={},
            ignore=[404, 400]
        )

        self.extend_options(options, search_type=search_type)

        response = self.client.search_template(**options)
        self.show_response(response)
