from pydantic import BaseModel,ConfigDict
from typing import Optional


class PropertyDetailsSchema(BaseModel):
    id: Optional[int]
    title: str
    property_type: str
    price: str
    area: str
    purpose: str
    location: str
    bedrooms: Optional[int]
    bathrooms: Optional[int]
    added: str

    model_config = ConfigDict(from_attributes=True)
