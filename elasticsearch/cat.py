from .utils import BaseClient
from .utils import make_path
from .utils import show_result


class CatClient(BaseClient):

    def aliases(self, name=None, params=None, command=None):
        result = self.client.request(
            'GET', make_path('_cat', 'aliases', name), params=params)
        return show_result(result.text, command)

    def allocation(self, node_id=None, params=None, command=None):
        result = self.client.request(
            'GET', make_path('_cat', 'allocation', node_id), params=params)
        return show_result(result.text, command)

    def count(self, index=None, params=None, command=None):
        result = self.client.request(
            'GET', make_path('_cat', 'count', index), params=params)
        return show_result(result.text, command)

    def health(self, params=None, command=None):
        result = self.client.request(
            'GET', make_path('_cat', 'health'), params=params)
        return show_result(result.text, command)

    def help(self, params=None, command=None):
        result = self.client.request(
            'GET', make_path('_cat'), params=params)
        return show_result(result.text, command)

    def indices(self, index=None, params=None, command=None):
        result = self.client.request(
            'GET', make_path('_cat', 'indices', index), params=params)
        return show_result(result.text, command)

    def master(self, params=None, command=None):
        result = self.client.request(
            'GET', make_path('_cat', 'master'), params=params)
        return show_result(result.text, command)

    def nodes(self, params=None, command=None):
        result = self.client.request(
            'GET', make_path('_cat', 'nodes'), params=params)
        return show_result(result.text, command)

    def recovery(self, index=None, params=None, command=None):
        result = self.client.request(
            'GET', make_path('_cat', 'recovery', index), params=params)
        return show_result(result.text, command)

    def shards(self, index=None, params=None, command=None):
        result = self.client.request(
            'GET', make_path('_cat', 'shards', index), params=params)
        return show_result(result.text, command)

    def segments(self, index=None, params=None, command=None):
        result = self.client.request(
            'GET', make_path('_cat', 'segments', index), params=params)
        return show_result(result.text, command)

    def pending_tasks(self, params=None, command=None):
        result = self.client.request(
            'GET', make_path('_cat', 'pending_tasks'), params=params)
        return show_result(result.text, command)

    def thread_pool(self, params=None, command=None):
        result = self.client.request(
            'GET', make_path('_cat', 'thread_pool'), params=params)
        return show_result(result.text, command)

    def fielddata(self, fields=None, params=None, command=None):
        result = self.client.request(
            'GET', make_path('_cat', 'fielddata', fields), params=params)
        return show_result(result.text, command)

    def plugins(self, params=None, command=None):
        result = self.client.request(
            'GET', make_path('_cat', 'plugins'), params=params)
        return show_result(result.text, command)
