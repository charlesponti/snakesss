from enum import Enum

class RoleName(Enum):
    ADMIN = "admin"
    MEMBER = "member"
    GUEST = "guest"

print(RoleName["ADMIN"].value)
