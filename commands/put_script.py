from .base import CreateBaseCommand


class PutScriptCommand(CreateBaseCommand):
    command_name = "elasticsearch:put-script"

    def parse_script_name(self, name):
        if name is None:
            return (None, None)

        try:
            lang, script_id = name.split("/")
        except ValueError:
            return (None, None)

        return (lang, script_id)

    def run_request(self, name=None):
        lang, script_id = self.parse_script_name(name)

        if not lang or not script_id:
            self.show_input_panel(
                'Script Name (format: lang/script_id): ',
                'groovy/indexedCalculateScore', self.run)
            return

        options = dict(
            lang=lang,
            id=script_id,
            body=self.get_text()
        )

        return self.client.put_script(**options)
