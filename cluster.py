from .base import ElasticsearchCommand


class ClusterInfoCommand(ElasticsearchCommand):
    result_window_title = "Cluster Info"

    def run(self):
        es = self.ESClient()
        self.request(es.info)


class ClusterHealthCommand(ElasticsearchCommand):
    result_window_title = "Cluster Health"

    def run(self):
        es = self.ESClient()
        self.request(es.cluster.health)


class ClusterPendingTasks(ElasticsearchCommand):
    result_window_title = "Cluster Pending Tasks"

    def run(self):
        es = self.ESClient()
        self.request(es.cluster.pending_tasks)


class ClusterStateCommand(ElasticsearchCommand):
    result_window_title = "Cluster State"

    def run(self):
        es = self.ESClient()
        self.request(es.cluster.state)


class ClusterStatsCommand(ElasticsearchCommand):
    result_window_title = "Cluster Stats"

    def run(self):
        es = self.ESClient()
        self.request(es.cluster.stats)


class ClusterRerouteCommand(ElasticsearchCommand):
    result_window_title = "Cluster Reroute"

    def run(self):
        es = self.ESClient()
        body = self.selection()
        self.request(es.cluster.reroute, body)


class GetClusterSettingsCommand(ElasticsearchCommand):
    result_window_title = "Get Cluster Settings"

    def run(self):
        es = self.ESClient()
        self.request(es.cluster.get_settings)


class PutClusterSettingsCommand(ElasticsearchCommand):
    result_window_title = "Put Cluster Settings"

    def run(self):
        es = self.ESClient()
        body = self.selection()
        self.request(es.cluster.put_settings, body)
