"""
Cat API Commdns for Elasticsearch Client for sublime text 3

For more information about API, see
http://www.elastic.co/guide/en/elasticsearch/reference/current/cat.html
"""

from .elasticsearch import ReusltTextCommand
from .elasticsearch import make_path


class ElasticsearchCatAliasesCommand(ReusltTextCommand):
    result_window_title = "** Elasticsearch: Aliases **"

    def run(self):
        path = make_path('_cat', 'aliases')
        self.request_get(path, params=dict(v=1))


class ElasticsearchCatAllocationCommand(ReusltTextCommand):
    result_window_title = "** Elasticsearch: Allocation **"

    def run(self):
        path = make_path('_cat', 'allocation')
        self.request_get(path, params=dict(v=1))


class ElasticsearchCatHealthCommand(ReusltTextCommand):
    result_window_title = "** Elasticsearch: Health **"

    def run(self):
        path = make_path('_cat', 'health')
        self.request_get(path, params=dict(v=1))


class ElasticsearchCatIndicesCommand(ReusltTextCommand):
    result_window_title = "** Elasticsearch: Indices **"

    def run(self):
        path = make_path('_cat', 'indices')
        self.request_get(path, params=dict(v=1, ts=0))


class ElasticsearchCatMasterCommand(ReusltTextCommand):
    result_window_title = "** Elasticsearch: Master **"

    def run(self):
        path = make_path('_cat', 'master')
        self.request_get(path, params=dict(v=1, ts=0))


class ElasticsearchCatNodesCommand(ReusltTextCommand):
    result_window_title = "** Elasticsearch: Nodes **"

    def run(self):
        path = make_path('_cat', 'nodes')
        self.request_get(path, params=dict(v=1))


class ElasticsearchCatPendingTasksCommand(ReusltTextCommand):
    result_window_title = "** Elasticsearch: Pending Tasks **"

    def run(self):
        path = make_path('_cat', 'pending_tasks')
        self.request_get(path, params=dict(v=1))


class ElasticsearchCatPluginsCommand(ReusltTextCommand):
    result_window_title = "** Elasticsearch: Plugins **"

    def run(self):
        path = make_path('_cat', 'plugins')
        self.request_get(path, params=dict(v=1))


class ElasticsearchCatRecoveryCommand(ReusltTextCommand):
    result_window_title = "** Elasticsearch: Recovery **"

    def run(self):
        path = make_path('_cat', 'recovery')
        self.request_get(path, params=dict(v=1))


class ElasticsearchCatSegmentsCommand(ReusltTextCommand):
    result_window_title = "** Elasticsearch: Segments **"

    def run(self):
        path = make_path('_cat', 'segments')
        self.request_get(path, params=dict(v=1))


class ElasticsearchCatShardsCommand(ReusltTextCommand):
    result_window_title = "** Elasticsearch: Shards **"

    def run(self):
        path = make_path('_cat', 'shards')
        self.request_get(path, params=dict(v=1))


class ElasticsearchCatThreadPoolCommand(ReusltTextCommand):
    result_window_title = "** Elasticsearch: Thread Pool **"

    def run(self):
        path = make_path('_cat', 'thread_pool')
        self.request_get(path, params=dict(v=1))
