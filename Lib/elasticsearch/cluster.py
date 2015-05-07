from .utils import BaseClient
from .utils import make_path
from .utils import show_result_json


class ClusterClient(BaseClient):
    def health(self, index=None, params=None, command=None):
        result = self.client.request(
            'GET', make_path('_cluster', 'health', index), params=params)
        return show_result_json(result.json(), command=command)

    def pending_tasks(self, params=None, command=None):
        result = self.client.request(
            'GET', make_path('_cluster', 'pending_tasks'), params=params)
        return show_result_json(result.json(), command=command)

    def state(self, metric=None, index=None, params=None, command=None):
        result = self.client.request(
            'GET', make_path('_cluster', 'state', metric, index),
            params=params)
        return show_result_json(result.json(), command=command)

    def stats(self, node_id=None, params=None, command=None):
        result = self.client.request(
            'GET', make_path('_cluster', 'stats', node_id),
            params=params)
        return show_result_json(result.json(), command=command)

    def reroute(self, body=None, params=None, command=None):
        result = self.client.request(
            'POST', make_path('_cluster', 'reroute'),
            body=body, params=params)
        return show_result_json(result.json(), command=command)

    def get_settings(self, params=None, command=None):
        result = self.client.request(
            'GET', make_path('_cluster', 'settings'), params=params)
        return show_result_json(result.json(), command=command)

    def put_settings(self, body, params=None, command=None):
        result = self.client.request(
            'PUT', make_path('_cluster', 'settings'), body=body, params=params)
        return show_result_json(result.json(), command=command)
