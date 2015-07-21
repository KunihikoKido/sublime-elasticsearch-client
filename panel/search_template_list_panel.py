import sublime


class SearchTemplateListPanel(object):

    def __init__(self, window, client):
        self.window = window
        self.client = client
        self.choices = []

    def on_done(self, index):
        if index == -1:
            return
        search_template = self.choices[index]
        self.callback(id=search_template[0])

    def show(self, callback):
        self.callback = callback

        options = dict(
            index=".scripts",
            doc_type="mustache"
        )

        try:
            response = self.client.search(**options)
        except Exception as e:
            return sublime.error_message("Error: {}".format(e))

        self.choices = []
        for doc in response["hits"]["hits"]:
            self.choices.append(doc["_id"])

        self.window.show_quick_panel(self.choices, self.on_done)
