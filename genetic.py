class Genetics:
    def __init__(self, resource_group_name, region, project, environment):
        self.resource_group_name = resource_group_name
        self.region = region
        self.project = project
        self.environment = environment
    
    def show_genetics(self):
        print(f'resource_group_name => {self.resource_group_name} \nregion => {self.region} \nproject => {self.project} \nenvironment => {self.environment}')