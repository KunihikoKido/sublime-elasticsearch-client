from .base import BaseCommand


class FieldStatsCommand(BaseCommand):
    command_name = "elasticsearch:field-stats"

    def is_enabled(self):
        return True

    def run_request(self, fields=None):
        if fields is None:
            self.show_input_panel(
                'a comma-separated list of fields (Option) : ', '', self.run)
            return

        options = dict(
            index=self.settings.index,
            params=dict(fields=fields),
            ignore=[400]
        )

        return self.client.field_stats(**options)
