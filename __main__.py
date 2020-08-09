from genetic import Genetics
from aks import AKS

genetics = Genetics(resource_group_name="pulumi-poc-rg",
                    location="westus",
                    project="pulumi-poc",
                    environment="dev"
                    )

rg = genetics.create_rg()

aks = AKS(cluster_count=2,
        location=rg.location,
        resource_group_name=rg.name,
        project=genetics.project, 
        environment=genetics.environment
        )

aks.create_cluster()
print(aks.cluster_names)
