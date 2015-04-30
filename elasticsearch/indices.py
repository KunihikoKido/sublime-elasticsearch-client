from .utils import BaseClient
from .utils import make_path
from .utils import show_result_json


class IndicesClient(BaseClient):

    def analyze(self, index=None, body=None, params=None, command=None):
        result = self.client.request(
            'POST', make_path(index, '_analyze'), body=body, params=params)
        return show_result_json(result.json(), command)

    def refresh(self, index=None, params=None, command=None):
        result = self.client.request(
            'POST', make_path(index, '_refresh'), params=params)
        return show_result_json(result.json(), command)

    def flush(self, index=None, params=None, command=None):
        result = self.client.request(
            'POST', make_path(index, '_flush'), params=params)
        return show_result_json(result.json(), command)

    def create(self, index, body=None, params=None, command=None):
        result = self.client.request(
            'PUT', make_path(index), body=body, params=params)
        return show_result_json(result.json(), command)

    def get(self, index, feature=None, params=None, command=None):
        result = self.client.request(
            'GET', make_path(index, feature), params=params)
        return show_result_json(result.json(), command)

    def open(self, index, params=None, command=None):
        result = self.client.request(
            'POST', make_path(index, '_open'), params=params)
        return show_result_json(result.json(), command)

    def close(self, index, params=None, command=None):
        result = self.client.request(
            'POST', make_path(index, '_close'), params=params)
        return show_result_json(result.json(), command)

    def delete(self, index, params=None, command=None):
        result = self.client.request(
            'DELETE', make_path(index), params=params)
        return show_result_json(result.json(), command)

    def put_mapping(self, index, doc_type, body, params=None, command=None):
        result = self.client.request(
            'PUT', make_path(index, '_mapping', doc_type),
            body=body, params=params)
        return show_result_json(result.json(), command)

    def get_mapping(self, index, doc_type, params=None, command=None):
        result = self.client.request(
            'GET', make_path(index, '_mapping', doc_type), params=params)
        return show_result_json(result.json(), command)

    def get_field_mapping(self, index, doc_type, field, params=None, command=None):
        result = self.client.request(
            'GET', make_path(index, '_mapping', doc_type, 'field', field),
            params=params)
        return show_result_json(result.json(), command)

    def delete_mapping(self, index, doc_type, params=None, command=None):
        result = self.client.request(
            'DELETE', make_path(index, '_mapping', doc_type), params=params)
        return show_result_json(result.json(), command)

    def put_alias(self, index, name, body=None, params=None, command=None):
        result = self.client.request(
            'PUT', make_path(index, '_alias', name),
            body=body, params=params)
        return show_result_json(result.json(), command)

    def get_alias(self, index=None, name=None, params=None, command=None):
        result = self.client.request(
            'GET', make_path(index, '_alias', name), params=params)
        return show_result_json(result.json(), command)

    def get_aliases(self, index=None, name=None, params=None, command=None):
        result = self.client.request(
            'GET', make_path(index, '_aliases', name), params=params)
        return show_result_json(result.json(), command)

    def update_aliases(self, body, params=None, command=None):
        result = self.client.request(
            'POST', make_path('_aliases'), body=body, params=params)
        return show_result_json(result.json(), command)

    def delete_alias(self, index, name, params=None, command=None):
        result = self.client.request(
            'DELETE', make_path(index, '_alias', name), params=params)
        return show_result_json(result.json(), command)

    def put_template(self, name, body, params=None, command=None):
        result = self.client.request(
            'PUT', make_path('_template', name), body=body, params=params)
        return show_result_json(result.json(), command)

    def get_template(self, name=None, params=None, command=None):
        result = self.client.request(
            'GET', make_path('_template', name), params=params)
        return show_result_json(result.json(), command)

    def delete_template(self, name, params=None, command=None):
        result = self.client.request(
            'DELETE', make_path('_template', name), params=params)
        return show_result_json(result.json(), command)

    def get_settings(self, index=None, name=None, params=None, command=None):
        result = self.client.request(
            'GET', make_path(index, '_settings', name), params=params)
        return show_result_json(result.json(), command)

    def put_settings(self, index, body, params=None, command=None):
        result = self.client.request(
            'PUT', make_path(index, '_settings'), body=body, params=params)
        return show_result_json(result.json(), command)

    def put_warmer(self, index, name, body, params=None, command=None):
        result = self.client.request(
            'PUT', make_path(index, '_warmer', name),
            body=body, params=params)
        return show_result_json(result.json(), command)

    def get_warmer(self, index, name=None, params=None, command=None):
        result = self.client.request(
            'GET', make_path(index, '_warmer', name), params=params)
        return show_result_json(result.json(), command)

    def delete_warmer(self, index, name, params=None, command=None):
        result = self.client.request(
            'DELETE', make_path(index, '_warmer', name), params=None)
        return show_result_json(result.json(), command)

    def status(self, index=None, params=None, command=None):
        result = self.client.request(
            'GET', make_path(index, '_status'), params=params)
        return show_result_json(result.json(), command)

    def stats(self, index=None, metric=None, params=None, command=None):
        result = self.client.request(
            'GET', make_path(index, '_stats', metric), params=params)
        return show_result_json(result.json(), command)

    def segments(self, index=None, params=None, command=None):
        result = self.client.request(
            'GET', make_path(index, '_segments'), params=params)
        return show_result_json(result.json(), command)

    def optimize(self, index=None, params=None, command=None):
        result = self.client.request(
            'POST', make_path(index, '_optimize'), params=params)
        return show_result_json(result.json(), command)

    def clear_cache(self, index=None, params=None, command=None):
        result = self.client.request(
            'POST', make_path(index, '_cache', 'clear'), params=params)
        return show_result_json(result.json(), command)

    def recovery(self, index=None, params=None, command=None):
        result = self.client.request(
            'GET', make_path(index, '_recovery'), params=params)
        return show_result_json(result.json(), command)

    def upgrade(self, index=None, params=None, command=None):
        result = self.client.request(
            'POST', make_path(index, '_upgrade'), params=params)
        return show_result_json(result.json(), command)

    def get_upgrade(self, index=None, params=None, command=None):
        result = self.client.request(
            'GET', make_path(index, '_upgrade'), params=params)
        return show_result_json(result.json(), command)
