import sublime


class DocTypeListPanel(object):

    def __init__(self, window, client, index):
        self.window = window
        self.client = client
        self.index = index
        self.choices = []

    def on_done(self, index):
        if index == -1:
            return
        self.callback(index=self.index, doc_type=self.choices[index])

    def show(self, callback):
        self.callback = callback

        options = dict(
            index=self.index,
            doc_type="_all"
            )

        try:
            response = self.client.indices.get_mapping(**options)
        except Exception as e:
            return sublime.error_message("Error: {}".format(e))

        mappings = []

        if "mappings" in response[self.index].keys():
            mappings = response[self.index]["mappings"].keys()

        for name in mappings:
            if name != "_default_":
                self.choices.append(name)
        self.choices.sort()
        self.window.show_quick_panel(self.choices, self.on_done)
