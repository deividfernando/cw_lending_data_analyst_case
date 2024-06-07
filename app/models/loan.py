from app.models import *
from app.models.base import Base

class LoanModel(Base):
    __tablename__ = 'loans'
    user_id = Column(Integer, ForeignKey('clients.user_id'), nullable=False)
    loan_id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    due_at = Column(DateTime, nullable=False)
    paid_at = Column(DateTime, nullable=True)
    status = Column(String(7), nullable=False)
    loan_amount = Column(Float, nullable=False)
    tax = Column(Float, nullable=False)
    due_amount = Column(Float, nullable=False)
    amount_paid = Column(Float, nullable=False, default=0)
    clients = relationship('ClientModel', back_populates='loans')