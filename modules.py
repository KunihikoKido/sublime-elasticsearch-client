from .base import ESClientBaseCommand


class PutScriptCommand(ESClientBaseCommand):
    result_window_title = "Put Script"

    def run(self):
        self.get_lang(self.on_done_lang)

    def on_done_lang(self, lang):
        if not lang:
            return

        self.lang = lang
        self.get_script_id(self.on_done)

    def on_done(self, id):
        if not id:
            return

        es = self.ESClient()
        body = self.selection()
        self.request(es.put_script, self.lang, id, body=body)


class GetScriptCommand(PutScriptCommand):
    result_window_title = "Get Script"

    def on_done(self, id):
        if not id:
            return

        es = self.ESClient()
        self.request(es.get_script, self.lang, id)


class DeleteScriptCommand(PutScriptCommand):
    result_window_title = "Delete Script"

    def on_done(self, id):
        if not id:
            return

        es = self.ESClient()
        self.request(es.delete_script, self.lang, id)
