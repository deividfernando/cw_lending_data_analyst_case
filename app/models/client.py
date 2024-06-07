from app.models import *
from app.models.base import Base

class ClientModel(Base):
    __tablename__ = 'clients'
    user_id = Column(Integer, autoincrement=True, primary_key=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    status = Column(String(8), nullable=False)
    batch = Column(Integer, nullable=False)
    credit_limit = Column(Integer, nullable=False)
    interest_rate = Column(Integer, nullable=False)
    denied_reason = Column(String(255), nullable=True)
    denied_at = Column(DateTime, nullable=True)
    loans = relationship('LoanModel', back_populates='clients')
