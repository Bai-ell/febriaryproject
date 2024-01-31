from pydantic import BaseModel, field_validator



class Item(BaseModel):
    id: int
    name: str
    salePriceU: float
    brand: str
    sale: int
    rating: int
    volume: int
    supplierId: int
    pics: int
    root: int
    feedback_count: int = None
    valuation: str = None
    
    @field_validator('salePriceU')
    def convert_sale_price(cls, sale_price:int):
        if sale_price is not None:
            return sale_price / 100
    
    
    
class Items(BaseModel):
    products: list[Item]

class Feedback(BaseModel):
    feedbackCountWithText: int
    valuation: str