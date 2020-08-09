import pulumi
import pulumi_azure as azure
from genetic import Genetics

class ACR(Genetics):
    def __init__(self, resource_count, resource_group_name, location, project, environment, tags):
        self.resorce_count = resource_count
        self.registry_names = []
        super().__init__(resource_group_name, location, project, environment, tags)

    def create_registry(self):
        for i in range(self.resorce_count):
            acr_name = f'pulumiacr{self.environment}{i}'
            acr = azure.containerservice.Registry(acr_name,
                name=acr_name,
                resource_group_name=self.resource_group_name,
                location=self.location,
                sku="Basic",
                admin_enabled=False,
                georeplication_locations=[
                    self.location
                ],
                tags=self.tags
                )
            
            self.registry_names.append(acr_name)
            