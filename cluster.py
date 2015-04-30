from .base import ESClientBaseCommand


class ClusterInfoCommand(ESClientBaseCommand):
    result_window_title = "Cluster Info"

    def run(self):
        es = self.ESClient()
        self.request(es.info)


class ClusterHealthCommand(ESClientBaseCommand):
    result_window_title = "Cluster Health"

    def run(self):
        es = self.ESClient()
        self.request(es.cluster.health)


class ClusterPendingTasks(ESClientBaseCommand):
    result_window_title = "Cluster Pending Tasks"

    def run(self):
        es = self.ESClient()
        self.request(es.cluster.pending_tasks)


class ClusterStateCommand(ESClientBaseCommand):
    result_window_title = "Cluster State"

    def run(self):
        es = self.ESClient()
        self.request(es.cluster.state)


class ClusterStatsCommand(ESClientBaseCommand):
    result_window_title = "Cluster Stats"

    def run(self):
        es = self.ESClient()
        self.request(es.cluster.stats)


class ClusterRerouteCommand(ESClientBaseCommand):
    result_window_title = "Cluster Reroute"

    def run(self):
        es = self.ESClient()
        body = self.selection()
        self.request(es.cluster.reroute, body)


class GetClusterSettingsCommand(ESClientBaseCommand):
    result_window_title = "Get Cluster Settings"

    def run(self):
        es = self.ESClient()
        self.request(es.cluster.get_settings)


class PutClusterSettingsCommand(ESClientBaseCommand):
    result_window_title = "Put Cluster Settings"

    def run(self):
        es = self.ESClient()
        body = self.selection()
        self.request(es.cluster.put_settings, body)
