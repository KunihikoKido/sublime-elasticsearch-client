import sublime


class ScriptListPanel(object):

    def __init__(self, window, client):
        self.window = window
        self.client = client
        self.choices = []

    def on_done(self, index):
        if index == -1:
            return
        script = self.choices[index]
        self.callback(lang=script[1], id=script[0])

    def show(self, callback):
        self.callback = callback

        options = dict(
            index=".scripts"
        )

        try:
            response = self.client.search(**options)
        except Exception as e:
            return sublime.error_message("Error: {}".format(e))

        self.choices = []
        for doc in response["hits"]["hits"]:
            self.choices.append([doc["_id"], doc["_type"]])
        self.choices.sort()
        self.window.show_quick_panel(self.choices, self.on_done)
