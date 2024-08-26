from datetime import date
from typing import List, Optional
import strawberry
from bson import ObjectId

@strawberry.type
class ProductType:
    _id: ObjectId = strawberry.field(
        default_factory=ObjectId, description='internal mongo id'
    )
    
    id: str = strawberry.field(
        default_factory=lambda: str(ObjectId()), description='unique product id'
    )
    
    title: str
    description: str
    photos: Optional[List[str]]
    price: float
    discount: Optional[float] = strawberry.field(default=0)
    added_at: date = strawberry.field(
        default_factory=date.today, description="User registration date"
    )
    
    @strawberry.field
    def total_price(self) -> float:
        if self.discount:
            return self.price * (1 - self.discount)
        return self.price
