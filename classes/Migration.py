import time
from .Workload import Workload
from .MountPoint import MountPoint
from .Credentials import Credentials

class Migration():
    '''
        PARAMS:
            @mountPoints = [MountPoint]
            @source: Workload
            @migration_target: MigrationTarget
            @state = string
    '''
    
    IS_C_ALLOWED = True

    def __init__(self, selected_mountPoints, source, target):

        if isinstance(selected_mountPoints, list) and isinstance(source, Workload):
            if isinstance(target, MigrationTarget) and False not in [isinstance(points, MountPoint) for points in selected_mountPoints]:

                self.selected_mountPoints = selected_mountPoints
                self.source = source
                self.target = target
                self.state = "preparing to start"
            
            else:
                raise ValueError
        
        else:
            raise ValueError
        
    def verify_source_storage(self):
        
        return True if False not in [mountPoint.name in [source.name for source in self.source.storage] for mountPoint in self.selected_mountPoints] else False
    
    def run(self):
        self.state = "running"
        
        if self.IS_C_ALLOWED and self.verify_source_storage():
            
            for source_storage in self.source.storage:
                if source_storage.name in [mount.name for mount in self.selected_mountPoints]:
                        self.target.vm_target.storage.append(source_storage)
                
            self.target.vm_target.ip = self.source.ip
            self.target.vm_target.credentials = self.source.credentials 
                
            time.sleep(60)
            
            self.state = "success"
        
        else:
            self.state = "error"
            
    def __str__(self):
        return "Migration:{}:{}:{}:{}".format(self.selected_mountPoints, self.source, self.target, self.state)

class Source():
    
    def __init__(self, ip, username, password):
        
        if ip is None or username is None or password is None:
            raise ValueError
            
        self.ip = ip
        self.username = username
        self.password = password
        
    def change_username(self, username):
        if username is None:
            raise ValueError
        
        self.username = username
        
    def change_password(self, password):
        if password is None:
            raise ValueError
        
        self.password = password
    
    def get_username(self):
        return self.username
    
    def get_password(self):
        return self.password
    
    def get_ip(self):
        return self.ip


class MigrationTarget():
    
    CLOUD_TYPES = ["aws", "azure", "vsphere", "vcloud"]
    
    def __init__(self, credentials, cloud_type, vm_target):

        if cloud_type in self.CLOUD_TYPES and isinstance(cloud_type, str):
            if isinstance(credentials, Credentials) and isinstance(vm_target, Workload):
                self.credentials = credentials
                self.cloud_type = cloud_type
                self.vm_target = vm_target
            
            else:
                raise ValueError
        else:
            raise ValueError

    def get_cloud_type(self):
        return self.cloud_type
        
    def __str__(self):
        return "MigrationTaget:{}:{}:{}".format(self.cloud_type, self.credentials, self.vm_target)
            
                    
        
        
        
        
