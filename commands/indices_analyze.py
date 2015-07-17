from .base import BaseCommand


class IndicesAnalyzeCommand(BaseCommand):

    def is_enabled(self):
        return True

    def run_request(self, analyzer=None):
        if analyzer is None:
            self.show_analyzer_list_panel(self.run_request)
            return

        options = dict(
            index=self.settings.index,
            analyzer=analyzer,
            body=self.get_text()
        )

        response = self.client.indices.analyze(**options)
        self.show_response(response)
