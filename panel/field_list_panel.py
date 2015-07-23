import sublime


class FieldListPanel(object):

    def __init__(self, window, client, index, doc_type):
        self.window = window
        self.client = client
        self.index = index
        self.doc_type = doc_type
        self.choices = []

    def on_done(self, index):
        if index == -1:
            return
        self.callback(field=self.choices[index])

    def show(self, callback):
        self.callback = callback

        options = dict(
            index=self.index,
            doc_type=self.doc_type,
            field="*"
        )

        try:
            response = self.client.indices.get_field_mapping(**options)
        except Exception as e:
            return sublime.error_message("Error: {}".format(e))

        self.choices = []

        for field in response[self.index]["mappings"][self.doc_type].keys():
            self.choices.append(field)
        self.choices.sort()
        self.window.show_quick_panel(self.choices, self.on_done)
