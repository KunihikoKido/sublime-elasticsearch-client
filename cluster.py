from .base import ElasticsearchCommand


class ClusterInfoCommand(ElasticsearchCommand):
    result_window_title = "Cluster Info"

    def run(self):
        self.request(self.esclient.info)


class ClusterHealthCommand(ElasticsearchCommand):
    result_window_title = "Cluster Health"

    def run(self):
        self.request(self.esclient.cluster.health)


class ClusterPendingTasks(ElasticsearchCommand):
    result_window_title = "Cluster Pending Tasks"

    def run(self):
        self.request(self.esclient.cluster.pending_tasks)


class ClusterStateCommand(ElasticsearchCommand):
    result_window_title = "Cluster State"

    def run(self):
        self.request(self.esclient.cluster.state)


class ClusterStatsCommand(ElasticsearchCommand):
    result_window_title = "Cluster Stats"

    def run(self):
        self.request(self.esclient.cluster.stats)


class ClusterRerouteCommand(ElasticsearchCommand):
    result_window_title = "Cluster Reroute"

    def run(self):
        body = self.selection()
        self.request(self.esclient.cluster.reroute, body)


class GetClusterSettingsCommand(ElasticsearchCommand):
    result_window_title = "Get Cluster Settings"

    def run(self):
        self.request(self.esclient.cluster.get_settings)


class PutClusterSettingsCommand(ElasticsearchCommand):
    result_window_title = "Put Cluster Settings"

    def run(self):
        body = self.selection()
        self.request(self.esclient.cluster.put_settings, body)
