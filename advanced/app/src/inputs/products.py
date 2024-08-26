from typing import List, Optional
import strawberry

@strawberry.input
class ProductInput:
    
    title: str
    
    description: str
    
    photos: Optional[List[str]]
    
    price: float


@strawberry.input
class ChangeProductDiscountInput:
    
    id: str
    
    discount: float

@strawberry.input
class ProductFilter:
    title: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None