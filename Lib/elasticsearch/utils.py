import json
from urllib.parse import urlencode

SKIP_PATH = (None, '', b'', [], ())


def make_path(*parts):
    return '/'.join([p for p in parts if p not in SKIP_PATH])


def make_url(base_url, path, params={}):
    query_string = urlencode(params or {})
    url = ''.join([base_url, path])

    if query_string:
        return '{0}?{1}'.format(url, query_string)

    return url


def bulk_body(body):
    if not body.endswith('\n'):
        body += '\n'
    return body


def show_result_json(obj, indent=4, sort_keys=False, command=None):
    if command is None:
        return obj

    text = json.dumps(
        obj, indent=indent, ensure_ascii=False, sort_keys=sort_keys)
    show_result(text, command)
    return obj


def show_result(text, command=None):
    if command is None:
        return text

    if command.show_result_on_window:
        panel = command.window.new_file()
        panel.set_name('**{}**'.format(command.result_window_title))
        panel.set_scratch(True)
    else:
        panel = command.window.\
            create_output_panel('elasticsearch')
        command.window.run_command(
            "show_panel", {"panel": "output.elasticsearch"})

    panel.set_syntax_file(command.syntax)
    panel.set_scratch(True)
    panel.set_read_only(False)
    panel.settings().set('gutter', True)
    panel.settings().set('line_numbers', True)
    panel.settings().set('word_wrap', False)
    panel.run_command('append', {'characters': text})
    panel.set_read_only(True)
    return text


class BaseClient(object):

    def __init__(self, client):
        self.client = client
