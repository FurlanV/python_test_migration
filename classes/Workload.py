from .MountPoint import MountPoint

class Workload():
    '''
        PARAMS:
            @ip: string
            @Credrentials: Credentials
            @Storage: [MountPoint]
    '''
    def __init__(self, ip, credentials, storage):
        
        if isinstance(ip, str) and isinstance(storage, list):
            
            if False not in [isinstance(point, MountPoint) for point in storage]:
                self.ip = ip
                self.credentials = credentials
                self.storage = storage
            else:
                raise ValueError
        
        else:
            raise ValueError        
    
    def __str__(self):
        return "Workload:{}:{}:{}".format(self.ip, self.credentials, self.storage)