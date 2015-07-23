from .base import BaseCommand


class GetScriptCommand(BaseCommand):
    command_name = "elasticsearch:get-script"

    def is_enabled(self):
        return True

    def run_request(self, lang=None, id=None):
        if not lang or not id:
            self.show_script_list_panel(self.run)
            return

        options = dict(
            lang=lang,
            id=id
        )

        return self.client.get_script(**options)
