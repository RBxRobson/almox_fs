import enum

class UserRole(str, enum.Enum):
    operator = "operator"
    manager = "manager"
    admin = "admin"