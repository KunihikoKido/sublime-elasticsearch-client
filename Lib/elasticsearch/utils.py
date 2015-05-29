import json
from urllib.parse import urlencode

SKIP_PATH = (None, '', b'', [], ())

string_types = str, bytes


def make_path(*parts):
    return '/'.join([p for p in parts if p not in SKIP_PATH])


def make_url(base_url, path, params={}):
    query_string = urlencode(params or {})
    url = ''.join([base_url, path])

    if query_string:
        return '{0}?{1}'.format(url, query_string)

    return url


def serialize_body(body):
    if isinstance(body, string_types):
        return body.encode('utf-8')

    if body is None:
        return None

    return json.dumps(body, ensure_ascii=False)


def bulk_body(body):
    if not body.endswith('\n'):
        body += '\n'
    return body


def show_result_json(obj, indent=4, sort_keys=True, command=None):
    if command is None:
        return obj

    text = json.dumps(
        obj, indent=indent, ensure_ascii=False, sort_keys=sort_keys)
    show_result(text, command)
    return obj


def show_result_table(text, padding=1, divider='|', header_div='-', command=None):

    def pad_to(unpadded, target_len):
        under = target_len - len(unpadded)
        if under <= 0:
            return unpadded
        return unpadded + (' ' * under)

    table = text.split('\n')
    table = [s.split() for s in table if s]
    output = ''

    longest_row_len = max([len(row) for row in table])

    for row in table:
        while len(row) < longest_row_len:
            row.append('')

    col_sizes = [max(map(len, col)) for col in zip(*table)]
    header_divs = [None] * len(col_sizes)
    num_cols = len(col_sizes)

    for cell_num in range(num_cols):
        header_divs[cell_num] = header_div * (col_sizes[cell_num] +
                                              padding * 2)

    if padding > 0:
        header_div_row = divider.join(header_divs)[padding:-padding]
    else:
        header_div_row = divider.join(header_divs)

    for row in table:
        for cell_num, cell in enumerate(row):
            row[cell_num] = pad_to(cell, col_sizes[cell_num])

    header = table[0]
    body = table[1:]

    multipad = ' ' * padding
    divider = multipad + divider + multipad
    output += divider.join(header) + '\n'
    output += header_div_row + '\n'
    for row in body:
        output += divider.join(row) + '\n'

    if output.endswith('\n'):
        output = output[:-1]

    show_result(output, command=command)


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
