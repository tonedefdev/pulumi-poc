from genetic import Genetics
from aks import AKS

genetics = Genetics(resource_group_name="pulumi-poc-rg",
                    location="westus",
                    project="pulumi-poc",
                    environment="dev",
                    tags={"Datacenter": "DC04"}
                    )

rg = genetics.create_rg()

aks = AKS(cluster_count=2,
        location=rg.location,
        resource_group_name=rg.name,
        project=genetics.project, 
        environment=genetics.environment,
        tags=genetics.tags
        )

aks.create_cluster()
print(aks.cluster_names)
