

class SwitchServerListPanel(object):

    def __init__(self, window, servers):
        self.window = window
        self.servers = servers
        self.choices = []

    def on_done(self, index):
        if index == -1:
            return
        self.callback(index)

    def show(self, callback):
        self.callback = callback

        for server in self.servers:
            self.choices.append([
                "{index}/{doc_type}".format(**server),
                "{base_url}".format(**server)
                ])
        self.window.show_quick_panel(self.choices, self.on_done)
