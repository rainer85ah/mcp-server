from pydantic import BaseModel


class Item(BaseModel):
    name: str
    price: float

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John",
                "price": 40
            }
        }
