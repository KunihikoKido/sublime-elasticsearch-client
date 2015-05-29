from .base import ElasticsearchCommand


class ClusterClientCommand(ElasticsearchCommand):
    def request_cluster_api(self, method, *args, **kwargs):
        method = getattr(self.esclient.cluster, method.lower())
        self.request(method, *args, **kwargs)


class ClusterInfoCommand(ElasticsearchCommand):
    result_window_title = "Cluster Info"

    def run(self):
        self.request_api('info')


class ClusterHealthCommand(ClusterClientCommand):
    result_window_title = "Cluster Health"

    def run(self):
        self.request_cluster_api('health')


class ClusterPendingTasks(ClusterClientCommand):
    result_window_title = "Cluster Pending Tasks"

    def run(self):
        self.request_cluster_api('pending_tasks')


class ClusterStateCommand(ClusterClientCommand):
    result_window_title = "Cluster State"

    def run(self):
        self.request_cluster_api('state')


class ClusterStatsCommand(ClusterClientCommand):
    result_window_title = "Cluster Stats"

    def run(self):
        self.request_cluster_api('stats')


class ClusterRerouteCommand(ClusterClientCommand):
    result_window_title = "Cluster Reroute"

    def is_enabled(self):
        return self.is_valid_json()

    def run(self):
        self.request_cluster_api('reroute', body=self.selection())


class GetClusterSettingsCommand(ClusterClientCommand):
    result_window_title = "Get Cluster Settings"

    def run(self):
        self.request_cluster_api('get_settings')


class PutClusterSettingsCommand(ClusterClientCommand):
    show_result_on_window = False
    result_window_title = "Put Cluster Settings"

    def is_enabled(self):
        return self.is_valid_json()

    def run(self):
        self.request_cluster_api('put_settings', body=self.selection())
