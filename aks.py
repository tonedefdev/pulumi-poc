import pulumi
import pulumi_azure as azure
from genetic import Genetics

class AKS(Genetics):
    def __init__(self, cluster_count, resource_group_name, location, project, environment):
        self.cluster_count = cluster_count
        super().__init__(resource_group_name, location, project, environment)

    def create_cluster(self):
        if self.environment == "prod":
            tags = {
                "Environment": "prod"
            }
        else:
            tags = {
                "Environment": "dev"
            }

        aks_name = f'{self.project}-aks-{self.environment}'
        dns_prefix = f'{aks_name}-{self.environment}'
        self.cluster_names = []

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
                tags=tags
                )

            cert = f'clientCertificate{i}'
            kubeConfig = f'kubeConfig{i}'
            pulumi.export(cert, pulumi_poc_aks.kube_configs[0]["clientCertificate"])
            pulumi.export(kubeConfig, pulumi_poc_aks.kube_config_raw)
            self.cluster_names.append(cluster_name)

    def get_kube_config(self, cluster_name):
        aks_cluster = azure.containerservice.get_kubernetes_cluster(name=cluster_name, resource_group_name=self.resource_group_name)
        print(aks_cluster.kube_config_raw)