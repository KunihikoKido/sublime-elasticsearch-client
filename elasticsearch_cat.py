"""
Cat API Commdns for Elasticsearch Client for sublime text 3

For more information about API, see
http://www.elastic.co/guide/en/elasticsearch/reference/current/cat.html
"""

from .elasticsearch import ReusltTextCommand
from .elasticsearch import make_path


class ElasticsearchCatAliasesCommand(ReusltTextCommand):

    def run(self):
        path = make_path('_cat', 'aliases')
        self.request_get(path, params=dict(v=1))


class ElasticsearchCatAllocationCommand(ReusltTextCommand):

    def run(self):
        path = make_path('_cat', 'allocation')
        self.request_get(path, params=dict(v=1))


class ElasticsearchCatHealthCommand(ReusltTextCommand):

    def run(self):
        path = make_path('_cat', 'health')
        self.request_get(path, params=dict(v=1))


class ElasticsearchCatIndicesCommand(ReusltTextCommand):

    def run(self):
        path = make_path('_cat', 'indices')
        self.request_get(path, params=dict(v=1, ts=0))


class ElasticsearchCatMasterCommand(ReusltTextCommand):

    def run(self):
        path = make_path('_cat', 'master')
        self.request_get(path, params=dict(v=1, ts=0))


class ElasticsearchCatNodesCommand(ReusltTextCommand):

    def run(self):
        path = make_path('_cat', 'nodes')
        self.request_get(path, params=dict(v=1))


class ElasticsearchCatPendingTasksCommand(ReusltTextCommand):

    def run(self):
        path = make_path('_cat', 'pending_tasks')
        self.request_get(path, params=dict(v=1))


class ElasticsearchCatPluginsCommand(ReusltTextCommand):

    def run(self):
        path = make_path('_cat', 'plugins')
        self.request_get(path, params=dict(v=1))


class ElasticsearchCatRecoveryCommand(ReusltTextCommand):

    def run(self):
        path = make_path('_cat', 'recovery')
        self.request_get(path, params=dict(v=1))


class ElasticsearchCatSegmentsCommand(ReusltTextCommand):

    def run(self):
        path = make_path('_cat', 'segments')
        self.request_get(path, params=dict(v=1))


class ElasticsearchCatShardsCommand(ReusltTextCommand):

    def run(self):
        path = make_path('_cat', 'shards')
        self.request_get(path, params=dict(v=1))


class ElasticsearchCatThreadPoolCommand(ReusltTextCommand):

    def run(self):
        path = make_path('_cat', 'thread_pool')
        self.request_get(path, params=dict(v=1))
