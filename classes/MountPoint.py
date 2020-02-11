class MountPoint():
    '''
        PARAMS:
            @name: string
            @size: int
    '''
    
    def __init__(self, name, size):
        if isinstance(name, str) and isinstance(size, int):
            self.name = name
            self.size = size
        else:
            raise ValueError
        
    def __str__(self):
        return "mountPoint:{}:{}".format(self.name, self.size)
    