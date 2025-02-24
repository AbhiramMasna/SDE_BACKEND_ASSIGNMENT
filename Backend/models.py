from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class RequestModel(Base):
    __tablename__ = "requests"
    id = Column(String, primary_key=True, index=True)
    status = Column(String, default="pending")
    images = relationship("ImageModel", back_populates="request")

class ImageModel(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, autoincrement=True)
    request_id = Column(String, ForeignKey("requests.id"))
    product_name = Column(String)
    input_url = Column(String)
    output_url = Column(String, nullable=True)
    status = Column(String, default="pending")
    request = relationship("RequestModel", back_populates="images")
