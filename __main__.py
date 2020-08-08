from genetic import Genetics
from aks import AKS

genetics = Genetics(resource_group_name="pulumi-poc",
                    region="westus",
                    project="pulumi-poc",
                    environment="dev"
                    )

aks = AKS(cluster_count=1, 
        resource_group_name=genetics.resource_group_name, 
        region=genetics.region, 
        project=genetics.project, 
        environment=genetics.environment
        )

aks.create_cluster()
aks.show_genetics()
