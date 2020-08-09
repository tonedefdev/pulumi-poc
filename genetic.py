import pulumi
import pulumi_azure as azure

class Genetics:
    def __init__(self, resource_group_name, location, project, environment):
        self.resource_group_name = resource_group_name
        self.location = location
        self.project = project
        self.environment = environment

    def create_rg(self):
        pulumi_poc_rg = azure.core.ResourceGroup(self.resource_group_name, name=self.resource_group_name, location=self.location)
        return pulumi_poc_rg
    
    def show_genetics(self):
        print(f'resource_group_name => {self.resource_group_name} \nlocation => {self.location} \nproject => {self.project} \nenvironment => {self.environment}')