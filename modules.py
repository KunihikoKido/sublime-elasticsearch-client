from .base import ElasticsearchCommand
from .base import delete_ok_cancel_dialog


class PutScriptCommand(ElasticsearchCommand):
    show_result_on_window = False
    result_window_title = "Put Script"

    def run(self):
        self.get_lang(self.on_done_lang)

    def on_done_lang(self, lang):
        self.lang = lang
        self.get_script_id(self.on_done)

    def on_done(self, id):
        self.request_api(
            'put_script', lang=self.lang, id=id, body=self.selection())


class GetScriptCommand(PutScriptCommand):
    result_window_title = "Get Script"

    def on_done(self, id):
        self.request_api('get_script', lang=self.lang, id=id)


class DeleteScriptCommand(PutScriptCommand):
    show_result_on_window = False
    result_window_title = "Delete Script"

    def on_done(self, id):
        if not delete_ok_cancel_dialog(id):
            return

        self.request_api('delete_script', lang=self.lang, id=id)
