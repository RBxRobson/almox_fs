import enum

class UserRole(str, enum.Enum):
    operator = "operator"
    manager = "manager"
    admin = "admin"

class MovementType(str, enum.Enum):
    entry = "entry"      
    exit = "exit"        
    adjustment = "adjustment" 