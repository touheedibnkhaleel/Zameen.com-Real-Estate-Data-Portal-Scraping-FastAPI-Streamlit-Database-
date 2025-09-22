from database import Base
from sqlalchemy import Column,Integer,Text

class PropertyDetails(Base):
    __tablename__ = 'property_details'

    id = Column(Integer,primary_key=True,nullable=False)
    title = Column(Text,nullable=False)
    property_type = Column(Text,nullable=False)
    price = Column(Text,nullable=False)
    area = Column(Text,nullable=False)
    purpose = Column(Text,nullable=False)
    location = Column(Text,nullable=False)
    bedrooms = Column(Integer,nullable=False)
    bathrooms = Column(Integer,nullable=False)
    added = Column(Text,nullable=False)