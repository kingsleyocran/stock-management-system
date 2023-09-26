import enum


class Gender(enum.Enum):
    male = "male"
    female = "female"


class Role(enum.Enum):
    customer = "customer"
    sales_rep = "sales_rep"


class ProductStatus(enum.Enum):
    available = "available"
    unavailable = "unavailable"


class OrderStatus(enum.Enum):
    delivered = "delivered"
    on_the_way = "on_the_way"
