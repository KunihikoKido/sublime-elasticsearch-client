import tempfile
import urllib.parse
from .base import BaseCommand


class HelperBenchmarkCommand(BaseCommand):
    command_name = "elasticsearch:helper-benchmark"

    def update_command_name(self, endpoint, search_type):
        if endpoint == "_search/template":
            self.command_name += "-for-search-template"
        else:
            self.command_name += "-for-search-request-body"

        if search_type:
            self.command_name += "-{}".format(search_type)

    def make_url(self, endpoint, params):
        url = "{base_url}/{index}/{doc_type}/{endpoint}".format(
                base_url=self.settings.base_url,
                index=self.settings.index,
                doc_type=self.settings.doc_type,
                endpoint=endpoint
            )
        url_parts = list(urllib.parse.urlparse(url))
        query = dict(urllib.parse.parse_qsl(url_parts[4]))
        params = dict([(k, v) for k, v in params.items() if v])
        query.update(params)
        url_parts[4] = urllib.parse.urlencode(query)
        return urllib.parse.urlunparse(url_parts)

    @property
    def postfile(self):
        file_name = self.window.active_view().file_name()
        if not file_name:
            text = self.get_text()
            temp = tempfile.NamedTemporaryFile(delete=False)
            temp.write(bytes(text, 'utf-8'))
            file_name = temp.name
            temp.close()
        return file_name

    def run_request(self, endpoint="_search", search_type=None):
        self.update_command_name(endpoint, search_type)

        cmd = [
            self.settings.ab_command,
            "-n", self.settings.ab_requests,
            "-c", self.settings.ab_concurrency
        ]

        for k, v in self.settings.headers.items():
            cmd += ["-H", "{0}: {1}".format(k, v)]

        cmd += ["-p", self.postfile]
        url = self.make_url(
            endpoint=endpoint,
            params=dict(search_type=search_type))
        cmd += [url]
        self.window.run_command('exec', {'cmd': cmd})
