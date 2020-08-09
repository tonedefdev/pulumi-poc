from genetic import Genetics
from aks import AKS

genetics = Genetics(resource_group_name="pulumi-poc-rg",
                    region="westus",
                    project="pulumi-poc",
                    environment="dev"
                    )

rg = genetics.create_rg()

aks = AKS(cluster_count=1,
        location=rg.location,
        resource_group_name=rg.name, 
        region=rg.location, 
        project=genetics.project, 
        environment=genetics.environment
        )

aks.create_cluster()
aks.show_genetics()
