#/usr/bin/python3

import pulumi
import pulumi_azure as azure

pulumi_poc_rg_name = "pulumi-poc-aks-rg"
project = "pulumi-poc"
location = "westus"
environment = "dev"
cluster_count = 3

if environment == "prod":
    tags = {
        "Environment": "prod"
    }
    aks_name = f'{project}-aks-{environment}'
    dns_prefix = f'{aks_name}-{environment}'
else:
    tags = {
        "Environment": "dev"
    }
    aks_name = f'{project}-aks-{environment}'
    dns_prefix = f'{aks_name}-{environment}'

pulumi_poc_rg=azure.core.ResourceGroup(pulumi_poc_rg_name, name=pulumi_poc_rg_name, location=location)

for i in range(cluster_count):
    cluster_name = f'{aks_name}{i}'
    dns_prefix_multi = f'{dns_prefix}{i}'
    pulumi_poc_aks=azure.containerservice.KubernetesCluster(cluster_name,
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

pulumi.export("clientCertificate", pulumi_poc_aks.kube_configs[0]["clientCertificate"])
pulumi.export("kubeConfig", pulumi_poc_aks.kube_config_raw)
