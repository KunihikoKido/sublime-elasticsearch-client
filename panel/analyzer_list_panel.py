import sublime


class AnalyzerListPanel(object):

    def __init__(self, window, client, index):
        self.window = window
        self.client = client
        self.index = index
        self.choices = []

    def on_done(self, index):
        if index == -1:
            return

        self.callback(analyzer=self.choices[index][0])

    def show(self, callback):
        self.callback = callback

        options = dict(
            index=self.index
        )

        try:
            response = self.client.indices.get_settings(**options)
        except Exception as e:
            return sublime.error_message("Error: {}".format(e))

        self.choices = DEFAULT_ANALYZERS.copy()

        analyzers = []

        try:
            analyzers = response[self.index]["settings"]["index"]["analysis"]["analyzer"].keys()
        except KeyError:
            pass

        for analyzer in analyzers:
            self.choices.append([
                analyzer,
                "Custom Analyzer: {}".format(analyzer)
                ])

        self.choices += DEFAULT_ANALYZERS
        self.choices.sort()
        self.window.show_quick_panel(self.choices, self.on_done)


DEFAULT_ANALYZERS = [
    ["standard", "Standard Analyzer: standard"],
    ["simple", "Simple Analyzer: simple"],
    ["whitespace", "Whitespace Analyzer: whitespace"],
    ["stop", "Stop Analyzer: stop"],
    ["keyword", "Keyword Analyzer: keyword"],
    ["pattern", "Pattern Analyzer: pattern"],
    ["snowball", "Snowball Analyzer: snowball"],
    ["arabic", "Language Analyzer: arabic"],
    ["armenian", "Language Analyzer: armenian"],
    ["basque", "Language Analyzer: basque"],
    ["brazilian", "Language Analyzer: brazilian"],
    ["bulgarian", "Language Analyzer: bulgarian"],
    ["catalan", "Language Analyzer: catalan"],
    ["chinese", "Language Analyzer: chinese"],
    ["cjk", "Language Analyzer: cjk"],
    ["czech", "Language Analyzer: czech"],
    ["danish", "Language Analyzer: danish"],
    ["dutch", "Language Analyzer: dutch"],
    ["english", "Language Analyzer: english"],
    ["finnish", "Language Analyzer: finnish"],
    ["french", "Language Analyzer: french"],
    ["galician", "Language Analyzer: galician"],
    ["german", "Language Analyzer: german"],
    ["greek", "Language Analyzer: greek"],
    ["hindi", "Language Analyzer: hindi"],
    ["hungarian", "Language Analyzer: hungarian"],
    ["indonesian", "Language Analyzer: indonesian"],
    ["irish", "Language Analyzer: irish"],
    ["italian", "Language Analyzer: italian"],
    ["latvian", "Language Analyzer: latvian"],
    ["norwegian", "Language Analyzer: norwegian"],
    ["persian", "Language Analyzer: persian"],
    ["portuguese", "Language Analyzer: portuguese"],
    ["romanian", "Language Analyzer: romanian"],
    ["russian", "Language Analyzer: russian"],
    ["sorani", "Language Analyzer: sorani"],
    ["spanish", "Language Analyzer: spanish"],
    ["swedish", "Language Analyzer: swedish"],
    ["turkish", "Language Analyzer: turkish"],
    ["thai", "Language Analyzer: thai"],
]
