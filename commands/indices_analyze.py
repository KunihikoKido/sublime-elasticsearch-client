from .base import BaseCommand


class IndicesAnalyzeCommand(BaseCommand):
    command_name = "elasticsearch:indices-analyze"

    def is_enabled(self):
        return True

    def run_request(self, analyzer=None):
        if analyzer is None:
            self.show_analyzer_list_panel(self.run)
            return

        options = dict(
            index=self.settings.index,
            analyzer=analyzer,
            body=self.get_text()
        )

        return self.client.indices.analyze(**options)
