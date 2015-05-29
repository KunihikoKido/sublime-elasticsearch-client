import sublime
import requests
from .cat import CatClient
from .indices import IndicesClient
from .cluster import ClusterClient
from .nodes import NodesClient
from .utils import make_url
from .utils import make_path
from .utils import show_result_json
from .utils import serialize_body
from .utils import bulk_body

MAX_RETRIES = 3


class Elasticsearch(object):

    def __init__(self, base_url='http://localhost:9200/', headers=None):
        self.base_url = base_url
        self.headers = headers

        self.cat = CatClient(self)
        self.indices = IndicesClient(self)
        self.cluster = ClusterClient(self)
        self.nodes = NodesClient(self)

    def request(self, method, path, body=None, params=None):
        url = make_url(self.base_url, path, params)
        body = serialize_body(body)

        session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(max_retries=MAX_RETRIES)
        session.mount(self.base_url, adapter)

        try:
            response = session.request(
                method.lower(), url, data=body,
                headers=self.headers, verify=False)

        except requests.exceptions.RequestException as e:
            import sys
            sublime.error_message("Error: {0!s}".format(e))
            sys.exit(1)

        return response

    def info(self, params=None, command=None):
        result = self.request(
            'GET', '/', params=params)
        return show_result_json(result.json(), command=command)

    def create(self, index, doc_type, body, id=None, params=None, command=None):
        params = params or {}
        params['op_type'] = 'create'
        return self.index(index, doc_type, body, id, params=params, command=command)

    def index(self, index, doc_type, body, id=None, params=None, command=None):
        method = 'PUT' if id else 'POST'
        result = self.request(
            method, make_path(index, doc_type, id), body=body, params=params)
        return show_result_json(result.json(), command=command)

    def get(self, index, doc_type, id, params=None, command=None):
        result = self.request(
            'GET', make_path(index, doc_type, id), params=params)
        return show_result_json(result.json(), command=command)

    def get_source(self, index, doc_type, id, params=None, command=None):
        result = self.request(
            'GET', make_path(index, doc_type, id, '_source'),
            params=params)
        return show_result_json(result.json(), command=command)

    def mget(self, body, index=None, doc_type=None, params=None, command=None):
        result = self.request(
            'POST', make_path(index, doc_type, '_mget'),
            body=body, params=params)
        return show_result_json(result.json(), command=command)

    def update(self, index, doc_type, id, body=None, params=None, command=None):
        result = self.request(
            'POST', make_path(index, doc_type, id, '_update'),
            body=body, params=params)
        return show_result_json(result.json(), command=command)

    def search(self, index=None, doc_type=None, body=None, params=None, command=None):
        if doc_type and not index:
            index = '_all'

        result = self.request(
            'POST', make_path(index, doc_type, '_search'),
            body=body, params=params)
        return show_result_json(result.json(), command=command)

    def search_shards(self, index=None, doc_type=None, params=None, command=None):
        result = self.request(
            'GET', make_path(index, doc_type, '_search_shards'),
            params=params)
        return show_result_json(result.json(), command=command)

    def search_template(self, index=None, doc_type=None, body=None, params=None, command=None):
        if doc_type and not index:
            index = '_all'

        result = self.request(
            'POST', make_path(index, doc_type, '_search', 'template'),
            body=body, params=params)
        return show_result_json(result.json(), command=command)

    def explain(self, index, doc_type, id, body=None, params=None, command=None):
        result = self.request(
            'POST', make_path(index, doc_type, id, '_explain'),
            body=body, params=params)
        return show_result_json(result.json(), command=command)

    def scroll(self, scroll_id, params=None, command=None):
        result = self.request(
            'POST', make_path('_search', 'scroll'),
            body=scroll_id, params=params)
        return show_result_json(result.json(), command=command)

    def clear_scroll(self, scroll_id, params=None, command=None):
        result = self.request(
            'DELETE', make_path('_search', 'scroll', scroll_id),
            params=params)
        return show_result_json(result.json(), command=command)

    def delete(self, index, doc_type, id, params=None, command=None):
        result = self.request(
            'DELETE', make_path(index, doc_type, id),
            params=params)
        return show_result_json(result.json(), command=command)

    def count(self, index=None, doc_type=None, body=None, params=None, command=None):
        result = self.request(
            'POST', make_path(index, doc_type, '_count'),
            params=params)
        return show_result_json(result.json(), command=command)

    def bulk(self, body, index=None, doc_type=None, params=None, command=None):
        result = self.request(
            'POST', make_path(index, doc_type, '_bulk'),
            body=bulk_body(body), params=params)
        return show_result_json(result.json(), command=command)

    def msearch(self, body, index=None, doc_type=None, params=None, command=None):
        result = self.request(
            'POST', make_path(index, doc_type, '_msearch'),
            body=body, params=params)
        return show_result_json(result.json(), command=command)

    def delete_by_query(self, index, doc_type=None, body=None, params=None, command=None):
        result = self.request(
            'DELETE', make_path(index, doc_type, '_query'),
            body=body, params=params)
        return show_result_json(result.json(), command=command)

    def suggest(self, body, index=None, params=None, command=None):
        result = self.request(
            'POST', make_path(index, '_suggest'),
            body=body, params=params)
        return show_result_json(result.json(), command=command)

    def percolate(self, index, doc_type, id=None, body=None, params=None, command=None):
        result = self.request(
            'POST', make_path(index, doc_type, id, '_percolate'),
            body=body, params=params)
        return show_result_json(result.json(), command=command)

    def mpercolate(self, body, index=None, doc_type=None, params=None, command=None):
        result = self.request(
            'POST', make_path(index, doc_type, '_mpercolate'),
            body=bulk_body(body), params=params)
        return show_result_json(result.json(), command=command)

    def count_percolate(self, index, doc_type, id=None, body=None, params=None, command=None):
        result = self.request(
            'POST', make_path(index, doc_type, id, '_percolate', 'count'),
            body=body, params=params)
        return show_result_json(result.json(), command=command)

    def mlt(self, index, doc_type, id, body=None, params=None, command=None):
        result = self.request(
            'POST', make_path(index, doc_type, id, '_mlt'),
            body=body, params=params)
        return show_result_json(result.json(), command=command)

    def termvectors(self, index, doc_type, id, body=None, params=None, command=None):
        result = self.request(
            'POST', make_path(index, doc_type, id, '_termvectors'),
            body=body, params=params)
        return show_result_json(result.json(), command=command)

    def termvector(self, index, doc_type, id, body=None, params=None, command=None):
        result = self.request(
            'POST', make_path(index, doc_type, id, '_termvector'),
            body=body, params=params)
        return show_result_json(result.json(), command=command)

    def mtermvectors(self, index=None, doc_type=None, body=None, params=None, command=None):
        result = self.request(
            'POST', make_path(index, doc_type, id, '_mtermvectors'),
            body=body, params=params)
        return show_result_json(result.json(), command=command)

    def benchmark(self, index=None, doc_type=None, body=None, params=None, command=None):
        result = self.request(
            'PUT', make_path(index, doc_type, '_bench'),
            body=body, params=params)
        return show_result_json(result.json(), command=command)

    def abort_benchmark(self, name=None, params=None, command=None):
        result = self.request(
            'POST', make_path('_bench', 'abort', name), params=params)
        return show_result_json(result.json(), command)

    def list_benchmarks(self, index=None, doc_type=None, params=None, command=None):
        result = self.request(
            'GET', make_path(index, doc_type, '_bench'), params=params)
        return show_result_json(result.json(), command=command)

    def put_script(self, lang, id, body, params=None, command=None):
        result = self.request(
            'PUT', make_path('_scripts', lang, id), body=body, params=params)
        return show_result_json(result.json(), command=command)

    def get_script(self, lang, id, params=None, command=None):
        result = self.request(
            'GET', make_path('_scripts', lang, id), params=params)
        return show_result_json(result.json(), command=command)

    def delete_script(self, lang, id, params=None, command=None):
        result = self.request(
            'DELETE', make_path('_scripts', lang, id), params=params)
        return show_result_json(result.json(), command=command)

    def put_template(self, id, body, params=None, command=None):
        result = self.request(
            'PUT', make_path('_search', 'template', id),
            body=body, params=params)
        return show_result_json(result.json(), command=command)

    def get_template(self, id, params=None, command=None):
        result = self.request(
            'GET', make_path('_search', 'template', id), params=params)
        return show_result_json(result.json(), command=command)

    def delete_template(self, id=None, params=None, command=None):
        result = self.request(
            'DELETE', make_path('_search', 'template', id), params=params)
        return show_result_json(result.json(), command=command)

    def search_exists(self, index=None, doc_type=None, body=None, params=None, command=None):
        result = self.request(
            'POST', make_path(index, doc_type, '_search', 'exists'),
            body=body, params=params)
        return show_result_json(result.json(), command=command)

    def validate_query(self, index=None, doc_type=None, body=None, params=None, command=None):
        result = self.request(
            'POST', make_path(index, doc_type, '_validate', 'query'),
            body=body, params=params)
        return show_result_json(result.json(), command=command)
