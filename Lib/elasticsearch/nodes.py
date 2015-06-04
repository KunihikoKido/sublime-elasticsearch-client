from .utils import BaseClient
from .utils import make_path
from .utils import show_result_json
from .utils import show_result


class NodesClient(BaseClient):
    def info(self, node_id=None, metric=None, params=None, command=None):
        result = self.client.request(
            'GET', make_path('_nodes', node_id, metric), params=params)
        return show_result_json(result.json(), command=command)

    def shutdown(self, node_id=None, params=None, command=None):
        result = self.client.request(
            'POST', make_path('_cluster', 'nodes', node_id, '_shutdown'),
            params=params)
        return show_result_json(result.json(), command=command)

    def stats(self, node_id=None, metric=None, index_metric=None, params=None, command=None):
        result = self.client.request(
            'GET',
            make_path('_nodes', node_id, 'stats', metric, index_metric),
            params=params)
        return show_result_json(result.json(), command=command)

    def hot_threads(self, node_id=None, params=None, command=None):
        result = self.client.request(
            'GET', make_path('_nodes', node_id, 'hot_threads'), params=params)
        return show_result(result.text, command=command)
