import pulumi
import pulumi_azure as azure
from genetic import Genetics

class AKS(Genetics):
    def __init__(self, cluster_count, resource_group_name, location, project, environment, tags):
        self.cluster_count = cluster_count
        self.cluster_names = []
        self.kube_configs = []
        super().__init__(resource_group_name, location, project, environment, tags)

    def create_cluster(self):
        aks_name = f'{self.project}-aks-{self.environment}'
        dns_prefix = f'{aks_name}-{self.environment}'

        for i in range(self.cluster_count):
            cluster_name = f'{aks_name}{i}'
            dns_prefix_multi = f'{dns_prefix}{i}'
            pulumi_poc_aks = azure.containerservice.KubernetesCluster(cluster_name,
                name=cluster_name,
                location=self.location,
                resource_group_name=self.resource_group_name,
                dns_prefix=dns_prefix_multi,
                default_node_pool={
                    "name": "default",
                    "node_count": 1,
                    "vm_size": "Standard_D2_v2",
                },
                identity={
                    "type": "SystemAssigned",
                },
                tags=self.tags
                )

            cert = f'clientCertificate{i}'
            kubeConfig = f'kubeConfig{i}'
            pulumi.export(cert, pulumi_poc_aks.kube_configs[0]["clientCertificate"])
            pulumi.export(kubeConfig, pulumi_poc_aks.kube_config_raw)
            self.cluster_names.append(cluster_name)
            self.kube_configs.append(pulumi_poc_aks.kube_config_raw)