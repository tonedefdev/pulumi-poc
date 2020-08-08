import pulumi
import pulumi_azure as azure
from genetic import Genetics

class AKS(Genetics):
    def __init__(self, cluster_count, resource_group_name, region, project, environment):
        self.cluster_count = cluster_count
        super().__init__(resource_group_name, region, project, environment)

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
        
        pulumi_poc_rg = azure.core.ResourceGroup(self.resource_group_name, name=self.resource_group_name, location=self.region)

        for i in range(self.cluster_count):
            cluster_name = f'{aks_name}{i}'
            dns_prefix_multi = f'{dns_prefix}{i}'
            pulumi_poc_aks = azure.containerservice.KubernetesCluster(cluster_name,
                name=cluster_name,
                location=pulumi_poc_rg.location,
                resource_group_name=pulumi_poc_rg.name,
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
            return print(f'Successfully built {cluster_name}')