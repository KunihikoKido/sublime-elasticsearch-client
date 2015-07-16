import sublime_plugin


class ShowOutputPanelCommand(sublime_plugin.WindowCommand):
    default_syntax = "Packages/Text/Plain text.tmLanguage"

    def run(self, text, syntax=None):
        if syntax is None:
            syntax = self.default_syntax

        panel = self.window.create_output_panel("elasticsearch")
        self.window.run_command(
            "show_panel", {"panel": "output.elasticsearch"})
        panel.set_syntax_file(syntax)
        panel.settings().set('gutter', True)
        panel.settings().set('word_wrap', False)
        panel.set_read_only(False)
        panel.run_command('append', {'characters': text})
        panel.set_read_only(True)
