


class UserDTO:
    def __init__(self, username: str, email: str, password: str, hashed_password: str):
        self.username = username
        self.email = email
        self.password = password
        self.hashed_password = hashed_password
        pass
    
    

class UserResponseDTO:
    def __init__(self, username: str, email: str, is_active: str, id: str):
        self.id = id
        self.username = username
        self.email = email
        self.is_active = is_active
        pass