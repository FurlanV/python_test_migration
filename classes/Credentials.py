class Credentials():
    '''
        PARAMS:
            @username: str
            @password: str
            @doamin: str
    '''
    def __init__(self, username, password, domain):
        if isinstance(username, str) and isinstance(password, str) and isinstance(domain,str):
            
            self.username = username
            self.password = password
            self.domain = domain
        else:
            raise ValueError
    
    def __str__(self):
        return "credentials:{}:{}:{}".format(self.username, self.password, self.domain)