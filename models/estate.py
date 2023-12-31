from . import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Double, BigInteger
from sqlalchemy.orm import relationship



class Estate(Base):
    # Tabela no SQL
    __tablename__ = "estates"
    # Atributos da classe
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String(100))
    dorms = Column(Double(), nullable=True)
    lat = Column(Double())
    lng = Column(Double())
    parking = Column(Double(), nullable=True)
    price = Column(Double(), nullable=True)
    toilets = Column(Double(), nullable=True)
    source = Column(String(10))
    source_id = Column(String(256))
    timestamp = Column(String(256))
    total_area = Column("total area", BigInteger(), nullable=True)
    estates_ind_id = Column(Integer, ForeignKey("estates_ind.id"))
    img = Column(String(255), nullable=True)
    estates_ind = relationship("EstatesInd")
    type = Column(String(255))
    district = Column(String(255))

    # Transforma no formato correto para visualização externa
    def to_view(self):
        return {
            "address": self.address,
            "district": self.district,
            "type": self.type,
            "dorms": self.dorms,
            "lat": self.lat,
            "lng": self.lng,
            "parking": self.parking,
            "price": self.price,
            "toilets": self.toilets,
            "source": self.source,
            "source_id": self.source_id,
            "timestamp": self.timestamp,
            "total_area": self.total_area,
            "estate_ind_id": self.estates_ind_id,
            "img": self.img
        }
